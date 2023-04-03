<script setup lang="ts">
import { ref, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router';

import { APP_NAME, loadCurrentUser } from '@/assets/ts/utils';
import { API } from '@/assets/ts/api';
import type { Game, User } from '@/assets/ts/interfaces';

const router = useRouter();

/* --- REFS --- */
let gameId = ref('');

let publicGames = ref([] as Game[]);

const $promisedUser: Promise<User> | Promise<null> | undefined = inject('promisedUser');
const currentUser = ref({} as User);
/* ------------ */

// Err. codes
let G2 = ref(false);

const getGame = () => {
    const gId = gameId.value;
    API.games.get(gId).then(data => {
        if (data.code !== 'G2')
            router.push({ name: 'game', params: { gId } });
        else
            G2.value = true;
    });
}

const createGame = () => {
    API.games.new(false, currentUser.value.id)
        .then(data => { 
            let gId = data?.game.id;
            router.push(`/game/${gId}`);
        })
        .catch(err => console.error(err));
}

onMounted(async () => {
    const pbGames = (await API.games.list(false, true)).games;
    publicGames.value = (<Game[]>pbGames).filter(g => { 
        return g.players.length >= 0 /* CHANGE HERE TO SHOW ONLY INTITIALIZATED GAMES (length = 1 instead of >= 0) */
    });
    await loadCurrentUser($promisedUser, currentUser);
})
</script>

<template>
    <div class="title">
        <h1>{{ APP_NAME }}</h1>
        <span class="sub-title">[BETA]</span>
    </div>
    <div class="centered">
        <div class="content">
            <h2 class="write-code">Entrez un code :</h2>
            <input v-model="gameId" placeholder="ex. : 4q04h92">
            <p v-if="G2">Game with ID '{{ gameId }}' doesn't exist :(</p>
            <div class="btns">
                <button type="submit" @click="$event => getGame">Go !</button>
                <button type="button">login/sign up</button>
            </div>
            <div class="create-game" v-if="!currentUser">
                <p><u>Vous devez avoir un compte afin de créer une partie.</u></p>
            </div>
            <div class="create-game" v-else>
                <p>...ou créez votre partie publique/privée.</p>
                <button @click="createGame">Nouvelle partie</button>
            </div>
            <p>Bienvenue sur cette réplique du fameux jeu <u>Puissance 4</u>, connu pour sa simplicité, sans prise de tête. <br>
            Ici, on préfère la prise de tête, raison pour laquelle on introduit avec cette reproduction un système compétitif, où celui gagnant le plus de 
            parties et obtenant le plus de points sera l'élu du classement !</p>
            <h2>Parties publiques : </h2>
            <div class="games" v-if="publicGames.length > 0">
                <div class="game" @click="$router.push(`/game/${game.id}`)" v-for="game in publicGames">
                    <p>Partie <span class="g-id">#{{ game.id }}</span></p>
                    <p class="created-by" v-if="game.owner">par 
                        <tippy 
                            placement="right"
                            interactive
                        >
                            {{ game.owner.name }}
                            <template #content>
                                <div class="profile" style="display: flex; align-items: center; gap: 15px;">
                                    <img 
                                        :src="game.owner.avatar_url" 
                                        alt="Avatar"
                                        width="25"
                                        height="25"
                                        style="border-radius: 50%"
                                    >
                                    <div class="p-infos" style="display: flex; flex-direction: column;">
                                        <span class="p-score">Score : {{ game.owner.score }}</span>
                                        <router-link :to="`/p/${game.owner.id}`" style="color: var(--link-blue);">Voir le profil</router-link>
                                    </div>
                                </div>
                            </template>
                        </tippy>
                    </p>
                    <p class="created-by" v-else>par Invité</p>
                </div>
            </div>
            <p v-else>Aucune partie publique n'est disponible :(</p>
        </div>
    </div>
</template>

<style scoped>
p {
    text-align: center;
}

.title {
    display: flex;
    flex-direction: column;
    margin-top: 1rem;
    margin-bottom: 3rem;
}

.title > h1 {
    font-family: 'Press Start 2P', cursive;
    color: var(--matrix-text);
    text-align: center;
    animation-duration: .8s;
    animation-name: blinking;
    animation-iteration-count: infinite;
    transition: none;
}

.title > .sub-title {
    text-align: center;
    font-family: 'Press Start 2P', cursive;
    font-size: 12px;
    color: var(--error-text);
}

h2 {
    padding-bottom: 20px;
}

.centered {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.centered > .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    max-width: 550px;
}

.content > input {
    outline: none;
    padding: 5px;
    border: 1px var(--matrix-text) solid;
    border-radius: 5px;
    font-family: 'Share Tech Mono', cursive;
    font-size: 16px;
    color: var(--text-color);
    background-color: rgb(31, 31, 31);
}

.content > ::placeholder {
    font-family: 'Share Tech Mono', cursive;
    color: var(--text-color);
}

.content h2 {
    color: var(--matrix-text);
    text-align: center;
}

.content > .write-code {
    overflow: hidden;
    white-space: nowrap;
    width: 16ch;
    animation: typing 4s steps(16, end);
}

.content > input[type=text] {
    background-color: var(--color-background);
    opacity: 0;
    color: var(--matrix-text);
    outline: none;
}

.content > .btns {
    display: flex;
    gap: 5px;
}

.content > .btns > button {
    font-family: 'Share Tech Mono', cursive;
    padding: 10px 20px;
    border-radius: 8px;
    border-style: solid;
    animation-duration: 4.1s;
    transition-duration: 0.4s;
}

.content > .btns > button[type='submit'] {
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
}

.content > .btns > button[type='submit']:hover {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.content > .btns > button[type='button'] {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.content > .btns > button[type='button']:hover {
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
    color: #000;
}

.content > .games {
    max-width: 550px;
    display: flex;
    gap: 20px;
    flex-flow: row wrap;
    justify-content: center;
}

.content > .games > .game {
    display: flex;
    flex-direction: column;
    background-color: var(--color-background-darker);
    padding: 10px;
    border-radius: 5px;
    border: 2px solid transparent;
    transition: 0.5s;
    cursor: pointer;
}

.content > .games > .game:hover {
    border: 2px solid var(--matrix-text);
}

.content > .games > .game > .created-by {
    cursor: default;
}

.content > .games > .game > p > .g-id {
    color: var(--color-small-text);
    font-size: 13px;
}

/* ANIMATIONS */

@keyframes typing {
    0% { width: 0; }
}

@keyframes blinking {
    0% {
        opacity: 1;
    }

    40% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}
</style>