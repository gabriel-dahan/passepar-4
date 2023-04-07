<script setup lang="ts">
import { onMounted, ref, inject, type Ref } from 'vue';
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router';
import { io } from 'socket.io-client';

import { API, getRawErrs, updateErrs } from '@/assets/ts/api';
import { matrixAsColumns } from '@/assets/ts/utils';

import type { Game, User } from '@/assets/ts/interfaces';

const route = useRoute();
const router = useRouter();
const id = route.params.id as string;

/* --- REFS --- */
const game = ref({} as Game);

const $promisedUser: Promise<User> | Promise<null> | undefined = inject('promisedUser');
const currentUser = ref({} as User);

const $socket = io('http://localhost:5000/game', { path: '/websocket' });

const errors = ref(getRawErrs());
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
    if(loadedGame.id) {
        loadedGame.matrix = matrixAsColumns(loadedGame.matrix);
        game.value = loadedGame;
    }
};

const initializeWSEvents = () => {
    $socket.on('connect', () => {
        $socket.emit('room_join', { room_id: game.value.id });
    });

    $socket.on('redirect', (route) => {
        router.push(route);
    });

    $socket.on('new_data', (new_game) => {
        game.value = new_game;
    });

    $socket.on('room_join', (room) => {
        console.log(`--- Connected - ${room} ---`)
    });
};

onMounted(async () => {
    await loadCurrentUser();
    await loadGameData();
    initializeWSEvents();
});

onBeforeRouteLeave((to, from, next) => {
    $socket.disconnect();
    console.log(`--- Disconnected - ${game.value.id} ---`)
    next();
});

const isPlayer = (userId: string) => {
    let check = false;
    game.value.players.forEach(player => {
        if(player.user.id === userId) 
            check = true;
    });
    return check;
};

/* --- PRE-GAME --- */ 

const deleteGame = () => {
    API.games.delete(id).then(data => {
        $socket.emit('redirect', '/');
    });
}

const joinGame = (color: number) => {
    let userId = currentUser.value ? currentUser.value.id : '';
    API.games.addplayer(id, color, userId)
        .then(data => {
            errors.value = getRawErrs();

            if(data?.game)
                $socket.emit('game_join', game.value.id)
            else if(data?.code)
                updateErrs(errors, data)
        });
};

/* ---------------- */ 


/* --- GAME --- */ 

const play = (column: number) => {
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
    <p class="guest-not-supported" v-if="!currentUser">Les utilisateurs invités ne sont pas encore supportés.</p>
    <!-- PRE-GAME SCREEN -->
    <div class="pre-game" v-else-if="game.id && game.status === 0">
        <p class="privacy public" v-if="game.public">Partie publique</p>
        <p class="privacy private" v-else>Partie privée</p>
        <button class="delete-game" @click="deleteGame" v-if="currentUser?.id === game.owner.id && game.players.length < 2">Supprimer la partie ?</button>
        <div class="main-content">
            <h1 class="game-title">Partie #{{ game.id }}</h1>
            <p class="players-count">Joueurs : <tippy placement="right" interactive>
                <span>{{ game.players.length }}/2</span>
                <template #content>
                    <div class="players" style="display: flex; flex-direction: column;" v-if="game.players.length > 0">
                        <span v-for="player in game.players">{{ player.user ? player.user.name : 'Invité' }} {{ player.user.id === game.owner.id ? '(hôte)' : '' }}</span>
                    </div>
                    <div v-else>
                        <span>Aucun joueur</span>
                    </div>
                </template>
            </tippy></p>
            <div class="pill-choice" v-if="game.players.length === 0 && currentUser.id === game.owner.id">
                <p>Choisissez la pilule de votre choix...</p>
                <div class="pills">
                    <img @click="joinGame(0)" src="@/assets/choices_left.png" alt="Red Pill">
                    <img @click="joinGame(1)" src="@/assets/choices_right.png" alt="Blue Pill">
                </div>
                <p class="error-msg" v-if="errors.G5">Finissez la partie en cours avant d'en rejoindre une nouvelle.</p>
            </div>
            <div class="pill-choice" v-else-if="game.players.length === 0">
                <p>Attendez que l'hôte choisisse sa couleur.</p>
            </div>
            <div class="game-join" v-else-if="game.players.length === 1 && !isPlayer(currentUser?.id)">
                <p>Il ne manque que vous !</p>
                <button class="start-game" @click="joinGame((game.players[0].color + 1) % 2)">Cliquez ici pour rejoindre la partie</button>
                <p>Attention, c'est un point de non retour...</p>
            </div>
            <div class="game-join" v-else-if="game.players.length === 1">
                <p>Attendez qu'un autre joueur rejoigne la partie...</p>
            </div>
            <div class="wait-room" v-else-if="game.players.length === 2 && game.status === 0 && game.owner.id === currentUser.id">
                <button>Lancer la partie ?</button>
            </div>
            <div class="wait-room" v-else>
                <p>Attendez que l'hôte lance la partie...</p>
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
    <div class="game" v-else-if="game.id && game.players.length === 2 && game.status === 1">
        <div id="grid">
            <!-- Loop goes from 1 to n (not 0 to n-1 in VueJS !), so we have to substract 1 to the index... -->
            <div :class="'column-' + (index - 1)" @click="play(index - 1)" v-for="index in game.matrix.length">
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

.pre-game > .delete-game {
    margin: 10px 0;
    background-color: transparent;
    font-size: 16px;
    border-radius: 5px;
    border: none;
    font-family: 'Share Tech Mono', cursive;
    color: #f15f5f;
    transition: 0.3s;
}

.pre-game > .delete-game:hover {
    transform: scale(0.9);
}

.pre-game > .main-content {
    gap: 5px;
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

.pre-game > .main-content > .pill-choice,
.pre-game > .main-content > .game-join {
    display: flex;
    gap: 20px;
    flex-direction: column;
}

.pre-game > .main-content > .game-join > .start-game {
    background-color: transparent;
    font-family: 'Share Tech Mono', cursive;
    color: #EE2E31;
    font-size: 16px;
    border: none;
    transition: 0.3s;
    cursor: pointer;
}

.pre-game > .main-content > .game-join > .start-game:hover {
    transform: scale(1.1);
}

.pre-game > .main-content > .pill-choice > .pills {
    display: flex;
    justify-content: center;
    gap: 100px;
}

.pre-game > .main-content > .pill-choice > .pills > img {
    height: 150px;
    width: auto;
    transition: transform 0.3s ease-out;
}

.pre-game > .main-content > .pill-choice > .pills > img:hover {
    transform: scale(1.2);
}

.pre-game > .connected-as {
    color: var(--color-small-text);
    font-size: 14px;
    margin-bottom: 10px;
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