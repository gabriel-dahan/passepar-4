<script setup lang="ts">
import { onMounted, ref, inject } from 'vue';
import { useRoute } from 'vue-router';

import { API } from '@/assets/ts/api';
import { matrixAsColumns } from '@/assets/ts/utils';

import type { Game, User } from '@/assets/ts/interfaces';

const route = useRoute();
const id = route.params.id as string;

/* --- REFS --- */
const game = ref({} as Game);

const $promisedUser: Promise<User> | Promise<null> | undefined = inject('promisedUser');
const currentUser = ref({} as User);
/* ------------ */

const loadCurrentUser = async () => {
    let user = await $promisedUser;
    if(user !== undefined)
        currentUser.value = user as User;
    else
        console.error('Current user cannot be loaded.')
};

const loadGameData = async () => {
    let loadedGame = await API.games.get(id);
    loadedGame.matrix = matrixAsColumns(loadedGame.matrix);
    game.value = loadedGame;
}

onMounted(async () => {
    await loadGameData();
    await loadCurrentUser();
});

/* --- PRE-GAME --- */ 

const colorChoice = (event: any, color: number) => {
    let userId = currentUser.value ? currentUser.value.id : '';
    API.games.addplayer(id, color, userId)
        .then(data => {
            console.log(data)
        });
}

/* ---------------- */ 


/* --- GAME --- */ 

const play = (event: any, column: number) => {
    API.games.play(id, String(column))
        .then(data => {
            loadGameData(); // Reloads the game's data.

            if(data.code && data.code === 'G3') {
                alert(`Column ${column + 1} is full.`) // Testing purposes.
            }
        })
        .catch(error => console.error(error));
};

/* ------------ */ 
</script>

<template>
    <!-- PRE-GAME SCREEN -->
    <div class="pre-game" v-if="game.id && game.players.length < 2">
        <p class="privacy public" v-if="game.public">Partie publique</p>
        <p class="privacy private" v-else>Partie privée</p>
        <div class="main-content">
            <h1 class="game-title">Partie #{{ game.id }}</h1>
            <p class="players-count">Joueurs : {{ game.players.length }}/2</p>
            <p>Choisissez la pilule de votre choix...</p>
            <div class="pill-choice">
                <img @click="colorChoice($event, 0)" src="@/assets/choices_left.png" alt="Red Pill">
                <img @click="colorChoice($event, 1)" src="@/assets/choices_right.png" alt="Blue Pill">
            </div>
        </div>
        <p class="connected-as" v-if="!currentUser">
            Vous jouez en tant qu'invité.
        </p>
        <p class="connected-as" v-else>
            Vous jouez en tant que <span class="username">{{ currentUser.name }}</span>
        </p>
    </div>

    <!-- STARTED GAME -->
    <div class="game" v-else-if="game.id && game.players.length === 2">
        <div id="grid">
            <!-- Loop goes from 1 to n (not 0 to n-1 in VueJS !), so we have to substract 1 to the index... -->
            <div :class="'column-' + (index - 1)" @click="play($event, index - 1)" v-for="index in game.matrix.length">
                <div class="cells">
                    <div class="cell" v-for="cell in game.matrix[index - 1]">
                        <img src="@/assets/pawn1.svg" alt="P1" v-if="cell == 1">
                        <img src="@/assets/pawn2.svg" alt="P2" v-else-if="cell == 2">
                        <img src="@/assets/void.svg" alt="NP" v-else>
                    </div>
                </div>
                <hr width="90%">
                <span class="col-num">{{ index }}</span>
            </div>
        </div>
        <p>Partie #{{ game.id }}</p>
    </div>
</template>

<style scoped>
.pre-game,
.pre-game > .main-content,
.game {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.pre-game p {
    font-family: 'Share Tech Mono', cursive;
    text-align: center;
}

.pre-game > .privacy {
    color: var(--color-text);
    padding: 0 7px;
    border-radius: 10px;
}

.pre-game > .privacy.public {
    border: 1px solid #297373;
}

.pre-game > .privacy.private {
    border: 1px solid #EE2E31;
}

.pre-game > .main-content > .game-title {
    font-family: 'Share Tech Mono', cursive;
    color: var(--matrix-text);
}

.pre-game > .main-content > .pill-choice {
    display: flex;
    justify-content: center;
    gap: 100px;
}

.pre-game > .main-content > .pill-choice > img {
    height: 150px;
    width: auto;
    transition: transform 0.3s ease-out;
}

.pre-game > .main-content > .pill-choice > img:hover {
    transform: scale(1.2);
}

.pre-game > .connected-as {
    color: var(--color-small-text);
    font-size: 14px;
}

.pre-game > .connected-as > .username {
    color: var(--matrix-text);
}

.game > #grid {
    justify-content: center;
    align-items: center;
    display: flex;
}

.game > #grid > [class^='column-'] {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 5px;
}

.game > #grid > [class^='column-'] > .col-num {
    font-family: 'VT323', monospace;
    font-size: 18px;
}

.game > #grid > [class^='column-'] > .cells {
    display: flex;
    flex-direction: column;
    border: 2px transparent solid;
    border-radius: 5px;
}

.game > #grid > [class^='column-']:hover > .cells {
    border: 2px var(--color-text) /*rgb(50, 238, 91) rgb(113, 113, 219) */ solid;
}


.game > #grid > [class^='column-'] > .cells > .cell {
    padding: 20px 30px;
}

.game > #grid > [class^='column-'] > .cells > .cell > img {
    user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    width: 50px;
    height: auto;
    rotate: -30deg;
}
</style>