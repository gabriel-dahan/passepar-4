<script setup lang="ts">
import { ref, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router';

import { APP_NAME, loadCurrentUser } from '@/assets/ts/utils';
import { API, getRawErrs, updateErrs } from '@/assets/ts/api';
import type { Game, User } from '@/assets/ts/interfaces';

const router = useRouter();

/* --- REFS --- */
let gameId = ref('');

let publicGames = ref([] as Game[]);

const $promisedUser: Promise<User> | Promise<null> | undefined = inject('promisedUser');
const currentUser = ref({} as User);

const errors = ref({
    ...getRawErrs(),
    invalidGameId: false
});
/* ------------ */

const getGame = () => {
    const gId = gameId.value;
    errors.value = {
        ...getRawErrs(),
        invalidGameId: false
    };
    if(!gId || gId.length !== 7) {
        errors.value.invalidGameId = true;
    } else {
        API.games.get(gId)
            .then(data => {
                if(data?.id)
                    router.push(`/game/${gId}`);
                else if(data?.code)
                    updateErrs(errors, data);
            });
    }
}

const createGame = () => {
    API.games.new(false, currentUser.value.id)
        .then(data => { 
            errors.value = {
                ...getRawErrs(),
                invalidGameId: false
            };
            if(data?.game) {
                let gId = data?.game.id;
                router.push(`/game/${gId}`);
            }
            else if(data && data.code)
                updateErrs(errors, data);
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
        <tippy placement="bottom" interactive>
            <span class="sub-title">[BETA]</span>
            <template #content>
                <p>Suggestion/bug ? <a href="https://mail.google.com/mail/u/0/#inbox?compose=new" target="_blank">work@gabrieldahan.me</a></p>
            </template>
        </tippy>
    </div>
    <div class="centered">
        <div class="content">
            <section class="general">
                <h2 class="write-code">Entrez un code :</h2>
                <input v-model="gameId" placeholder="ex. : 4q04h92">
                <p class="error-msg" v-if="errors.G2">La partie demandée n'existe pas :(</p>
                <p class="error-msg" v-else-if="errors.invalidGameId">L'identifiant entré est incorrect...</p>
                <div class="btns">
                    <button class="join-game" @click="$event => getGame()">GO !</button>
                    <button class="login-or-register" @click="router.push('/login')">login/sign up</button>
                </div>
                <div class="create-game" v-if="!currentUser">
                    <p><u>Vous devez avoir un compte afin de créer une partie.</u></p>
                </div>
                <div v-else-if="currentUser.game_id">
                    <p><i>Partie en cours</i> : <router-link :to="`/game/${currentUser.game_id}`">Rejoindre</router-link></p>
                </div>
                <div class="create-game" v-else>
                    <p>...ou créez votre partie publique/privée.</p>
                    <button class="new-game" @click="createGame">Nouvelle partie</button>
                    <p class="error-msg" v-if="errors.G5">Vous êtes déjà hôte d'une autre partie.</p>
                </div>
                <p>Bienvenue sur cette réplique du fameux jeu <tippy interactive>
                    <u>Puissance 4</u>
                    <template #content>
                        Voir <a href="https://fr.wikipedia.org/wiki/Puissance_4" target="_blank" style="color: var(--link-blue);">
                            ici<img src="@/assets/external-link.svg" alt="" width="13">
                        </a>
                    </template>
                </tippy>, connu pour sa simplicité, sans prise de tête. <br>
                Ici, on préfère la prise de tête, raison pour laquelle on introduit avec cette reproduction un système compétitif, où celui gagnant le plus de 
                parties et obtenant le plus de points sera l'élu du classement !</p>
            </section>
            <section class="public-games">
            <h2>Parties publiques : </h2>
                <div class="games" v-if="publicGames.length > 0">
                    <div class="game" @click="$router.push(`/game/${game.id}`)" v-for="game in publicGames">
                        <p>Partie <span class="g-id">#{{ game.id }}</span></p> 
                            <p class="created-by" v-if="game.owner"> par 
                            <tippy 
                                placement="right"
                                interactive
                            >
                                <p class="game-owner">{{ game.owner.short_name }}</p>
                                <template #content>
                                    <div class="profile" style="display: flex; align-items: center; gap: 15px; width: max-content;">
                                        <img 
                                            :src="game.owner.avatar_url" 
                                            alt="Avatar"
                                            width="25"
                                            height="25"
                                            style="border-radius: 50%"
                                        >
                                        <div class="p-infos" style="display: flex; flex-direction: column;">
                                            <router-link :to="`/p/${game.owner.id}`" style="color: var(--link-blue);" @click.stop>{{ game.owner.name }}</router-link>
                                            <span class="p-score">Score : {{ game.owner.score }}</span>
                                        </div>
                                    </div>
                                </template>
                            </tippy>
                        </p>
                        <p class="created-by" v-else>par Invité</p>
                    </div>
                </div>
                <p v-else>Aucune partie publique n'est disponible :(</p>
            </section>
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

.title > span {
    text-align: center;
}

.title > span > .sub-title {
    font-family: 'Press Start 2P', cursive;
    font-size: 12px;
    color: var(--error-text);
}

h2 {
    padding-bottom: 10px;
}

.centered {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 35px;
    max-width: 550px;
}

.content > .general {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}

.content > .general > .create-game {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.content > .general > .create-game > .new-game {
    outline: none;
    margin: 10px 0;
    padding: 5px;
    border: none;
    border-radius: 10px;
    font-family: 'Share Tech Mono', cursive;
    font-size: 14px;
    color: var(--matrix-text);
    background-color: transparent;
    transition: 0.3s;
    cursor: pointer;
}

.content > .general > .create-game > .new-game:hover {
    transform: scale(1.1);
}

.content > .general > input {
    outline: none;
    padding: 5px;
    border: 1px var(--matrix-text) solid;
    border-radius: 5px;
    font-family: 'Share Tech Mono', cursive;
    font-size: 16px;
    color: var(--text-color);
    background-color: rgb(31, 31, 31);
}

.content > .general > ::placeholder {
    font-family: 'Share Tech Mono', cursive;
    color: var(--text-color);
}

.content h2 {
    color: var(--matrix-text);
    text-align: center;
}

.content > .general > .write-code {
    overflow: hidden;
    white-space: nowrap;
    width: 16ch;
    animation: typing 4s steps(16, end);
}

.content > .general > input[type=text] {
    background-color: var(--color-background);
    opacity: 0;
    color: var(--matrix-text);
    outline: none;
}

.content > .general > .btns {
    display: flex;
    gap: 5px;
}

.content > .general > .btns > button {
    font-family: 'Share Tech Mono', cursive;
    padding: 10px 20px;
    border-radius: 8px;
    border-style: solid;
    animation-duration: 4.1s;
    transition-duration: 0.4s;
}

.content > .general > .btns > button.join-game {
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
}

.content > .general > .btns > button.join-game:hover {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.content > .general > .btns > button.login-or-register {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.content > .general > .btns > button.login-or-register:hover {
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
    color: #000;
}

.content > .public-games {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.content > .public-games > .games {
    max-width: 550px;
    display: flex;
    gap: 20px;
    flex-flow: row wrap;
    justify-content: center;
}

.content > .public-games > .games > .game {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 150px;
    height: 80px;
    background-color: var(--color-background-darker);
    padding: 10px;
    border-radius: 5px;
    border: 2px solid transparent;
    transition: 0.5s;
    cursor: pointer;
}

.content > .public-games > .games > .game:hover {
    border: 2px solid var(--matrix-text);
}

.content > .public-games > .games > .game > .created-by {
    display: flex;
    gap: 10px;
    cursor: default;
}

.content > .public-games > .games > .game > .created-by .game-owner {
    transition: 0.3s;
}

.content > .public-games > .games > .game > .created-by .game-owner:hover {
    color: #fff;
}

.content > .public-games > .games > .game > p > .g-id {
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