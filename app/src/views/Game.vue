<script setup lang="ts">
import { onMounted, ref, inject, type Ref } from 'vue';
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router';
import { Socket, io } from 'socket.io-client';

import { API, getRawErrs, updateErrs } from '@/assets/ts/api';
import { matrixAsColumns, loadCurrentUser } from '@/assets/ts/utils';

import type { Game, User } from '@/assets/ts/interfaces';

const route = useRoute();
const router = useRouter();
const id = route.params.id as string;

/* --- REFS --- */
const game = ref({} as Game);

const $promisedUser: Promise<User> | Promise<null> | undefined = inject('promisedUser');
const currentUser = ref({} as User);

const errors = ref(getRawErrs());
/* ------------ */

let $socket: Socket = io();
const initializeSocketConn = () => {
    $socket = io(`http://127.0.0.1:8001/game`, {
        path: '/websocket'
    });
}

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

    $socket.on('redirect', (data) => {
        router.push(data.route).then(() => {
            if(data.reload)
                router.go(0);
        });
    });

    $socket.on('new_data', (new_game) => {
        // Changes the game data's matrix to make it easier to manipulate in game.
        new_game.matrix = matrixAsColumns(new_game.matrix); 
        game.value = new_game;
    });

    $socket.on('end_game', (winner) => {
        API.games.delete(game.value.id).then(data => {
            const endGameElem = document.getElementById('end-game');
            endGameElem?.classList.add('active');
            // router.push('/');
        });
    });
};

onMounted(async () => {
    await loadCurrentUser($promisedUser, currentUser);
    await loadGameData();
    initializeSocketConn();
    initializeWSEvents();
});

onBeforeRouteLeave((to, from, next) => {
    $socket.disconnect();
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

const changeGamePrivacy = () => {
    $socket.emit('change_privacy', game.value.id);
} 

const deleteGame = () => {
    API.games.delete(id).then(data => {
        $socket.emit('redirect', {
            route: '/', reload: true
        }, game.value.id);
    });
}

const joinGame = (color: number) => {
    let userId = currentUser.value ? currentUser.value.id : '';
    API.games.addplayer(id, color, userId)
        .then(data => {
            errors.value = getRawErrs();

            if(data?.game)
                $socket.emit('game_join', game.value.id);
            else if(data?.code)
                updateErrs(errors, data);
        });
};

const launchGame = () => {
    $socket.emit('launch_game', game.value.id);
}

/* ---------------- */ 


/* --- GAME --- */ 

const shakeColumn = (column: number, shakeTime: number = 300) => {
    const columnElem: HTMLDivElement | null = document.querySelector(`.column-${column}`);
    if(columnElem) {
        columnElem.classList.add('shake');
        setTimeout(() => {
            columnElem.classList.remove('shake');
        }, shakeTime);
    }
}

const play = (column: number) => {
    if(currentUser.value.id === game.value.players[game.value.turn - 1].user.id) {
        API.games.play(game.value.id, String(column))
            .then(data => {
                $socket.emit('play', game.value.id);
                if(data.code && data.code === 'G3')
                    shakeColumn(column)
            })
            .catch(error => console.error(error));
    } else 
        shakeColumn(column)
};

const leaveGame = () => {
    API.games.delete(id).then(game => {
        API.users.add_score(currentUser.value.id, -20).then(user => {
            $socket.emit('redirect', {
                route: '/', 
                reload: true
            }, game.id);
        })
    });
}

/* ------------ */ 
</script>

<template>
    <div class="game-room" v-if="game?.id">
        <div id="end-game">
            <img src="@/assets/passepartout.jpeg" alt="passepartout" class="passepartout">
            <h1>GAME OVER</h1>
        </div>
        <div class="change-privacy" v-if="game.public">
            <p class="privacy public" >Partie publique</p>
            <button 
                @click="changeGamePrivacy"
                v-if="game.status === 0 && game.owner.id === currentUser?.id"
            >
                Changer ?
            </button>
        </div>
        <div class="change-privacy" v-else>
            <p class="privacy private">Partie privée</p>
            <button 
                @click="changeGamePrivacy"
                v-if="game.status === 0 && game.owner.id === currentUser?.id"
            >
                Changer ?
            </button>
        </div>
        
        
        <p class="guest-not-supported" v-if="!currentUser">Les utilisateurs invités ne sont pas encore supportés.</p>
        <p class="not-authorized" v-else-if="currentUser.id !== game.owner.id && !isPlayer(currentUser.id) && currentUser.game_id">
            Finissez votre partie en cours pour en rejoindre une nouvelle !
        </p>
        <!-- PRE-GAME SCREEN -->
        <div class="pre-game" v-else-if="game.status === 0">
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
                    <button class="join-btn" @click="joinGame((game.players[0].color + 1) % 2)">Cliquez ici pour rejoindre la partie</button>
                    <p>Attention, c'est un point de non retour...</p>
                </div>
                <div class="game-join" v-else-if="game.players.length === 1">
                    <p>Attendez qu'un autre joueur rejoigne la partie...</p>
                </div>
                <div class="wait-room" v-else-if="game.players.length === 2 && game.status === 0 && game.owner.id === currentUser.id">
                    <button class="launch-game" @click="launchGame">Lancer la partie ?</button>
                </div>
                <div v-else-if="game.players.length === 2 && game.status === 0 && isPlayer(currentUser.id)">
                    <p>Attendez que l'hôte lance la partie...</p>
                </div>
            </div>
        </div>

        <!-- STARTED GAME -->
        <div class="game" v-else-if="game.id && game.players.length === 2 && game.status === 1 && isPlayer(currentUser.id)">
            <p>Tour : <span :style="`color: ${game.turn === 1 + game.players[0].color ? 'var(--vt-c-soft-red)' : 'var(--vt-c-soft-blue-1)'};`">{{ game.players[game.turn - 1].user.name }}</span></p>
            <div id="grid" >
                <!-- Loop goes from 1 to n (not 0 to n-1 in VueJS !), so we have to substract 1 to the index... -->
                <div :class="'column-' + (index - 1)" @click="play(index - 1)" v-for="index in game.matrix.length">
                    <div class="cells" @mouseover.capture>
                        <!-- If the color of the game owner is red -->
                        <div class="cell" v-for="cell in game.matrix[index - 1]" v-if="game.players[0].color === 0"> 
                            <img src="@/assets/pawn1.svg" alt="P1" v-if="cell == 1">
                            <img src="@/assets/pawn2.svg" alt="P2" v-else-if="cell == 2">
                            <img src="@/assets/void.svg" alt="NP" v-else>
                        </div>
                        <!-- Else -->
                        <div class="cell" v-for="cell in game.matrix[index - 1]" v-else> 
                            <img src="@/assets/pawn1.svg" alt="P1" v-if="cell == 2">
                            <img src="@/assets/pawn2.svg" alt="P2" v-else-if="cell == 1">
                            <img src="@/assets/void.svg" alt="NP" v-else>
                        </div>
                    </div>
                    <hr width="90%">
                    <span class="col-num">{{ index }}</span>
                </div>
            </div>
            <p>Partie #{{ game.id }}</p>
            <tippy placement="bottom" trigger="click" interactive>
                <button class="leave-game">Quitter la partie</button>
                <template #content>
                    <p class="error-msg">/!\ Quitter une partie en cours entraine une pénalité de points. <button class="confirm-leave" @click="leaveGame">Confirmer</button></p>
                </template>
            </tippy>
        </div>
        <div v-else>
            <p>Cette partie est en cours...</p>
        </div>
        <p class="connected-as" v-if="!currentUser">
            Vous jouez en tant qu'invité.
        </p>
        <p class="connected-as" v-else>
            Vous jouez en tant que <span class="username">{{ currentUser.name }}</span>
        </p>
    </div>
    <div v-else>
        <p>Cette partie est finie ou n'existe pas...</p>
    </div>
</template>

<style scoped>

#end-game {
    background-color: rgba(0, 0, 0, 0.8);
    width: 100%;
    height: 100%;
    z-index: 100;
    position: absolute;
    display: none;
    transition: 0.5s;
}

#end-game.active {
    display: flex;
    flex-direction: column;
    gap: 200px;
    align-items: center;
    justify-content: center;
}

#end-game > .passepartout {
    width: 20px;
    animation: rotation 3s, disappear 4s 1s;
}

#end-game > h1 {
    color: var(--matrix-text);
    font-family: 'Press Start 2P', cursive;
}

.game-room > #end-game.active {
    background: rgba(0, 0, 0, 0.8);
}

@keyframes rotation {
    0% {
        transform : rotate(1deg) scale(1);
    }
    100% {
        transform: rotate(1080deg) scale(20);
    }
}

@keyframes disappear {
    0% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}

.game-room {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 40px;
    align-items: center;
}

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

.change-privacy {
    display: flex;
    flex-direction: column;
    gap: 5px;
    align-items: center;
}

.change-privacy > button {
    background-color: transparent;
    border: none;
    color: var(--color-small-text);
    font-family: 'Share Tech Mono', cursive;
    transition: 0.3s;
}

.change-privacy > button:hover {
    color: var(--color-text);
    animation: shake 0.3s;
}

.privacy {
    color: var(--color-text);
    padding: 0 7px;
    border-radius: 10px;
}

.privacy.public {
    border: 1px solid #297373;
}

.privacy.private {
    border: 1px solid #f15f5f;
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

.pre-game > .main-content > .game-join > .join-btn {
    background-color: transparent;
    font-family: 'Share Tech Mono', cursive;
    color: #f15f5f;
    font-size: 16px;
    border: none;
    transition: 0.3s;
    cursor: pointer;
}

.pre-game > .main-content > .game-join > .join-btn:hover {
    transform: scale(1.1);
}

.pre-game > .main-content > .wait-room > .launch-game {
    margin-top: 15px;
    padding: 3px 5px;
    border: 2px solid var(--matrix-text);
    border-radius: 5px;
    font-family: 'Share Tech Mono', cursive;
    color: var(--matrix-text);
    background-color: #297373;
}

.pre-game > .main-content > .wait-room > .launch-game:hover {
    border-color: #297373;
    color: #297373;
    background-color: var(--matrix-text);
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

.connected-as {
    color: var(--color-small-text);
    font-size: 14px;
    margin-bottom: 10px;
}

.connected-as > .username {
    color: var(--matrix-text);
}

.game {
    gap: 30px;
}

.game .leave-game {
    font-family: 'Share Tech Mono', cursive;
    color: var(--error-text);
    border-radius: 5px;
    border: 2px dashed var(--error-text);
    background-color: transparent;
    padding: 3px 5px;
}

.game .leave-game:hover {
    animation: shake 0.2s;
}

.game .confirm-leave {
    font-family: 'Share Tech Mono', cursive;
    background-color: transparent;
    color: var(--link-blue);
    border: none;
    text-decoration: underline;
}

.game .confirm-leave:hover {
    font-style: italic;
}

.game > #grid {
    justify-content: center;
    align-items: center;
    display: flex;
    gap: 5px;
}

.game > #grid > [class^='column-'] {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 5px;
}

.game > #grid > [class^='column-'].shake:hover > .cells {
    border: 2px #f15f5f solid;
    animation: shake 0.3s;
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
    transition: 0.4s;
}

.game > #grid > [class^='column-']:hover > .cells {
    border: 2px var(--color-text) solid;
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

@keyframes shake {
    0% { transform: translateX(0) }
    25% { transform: translateX(5px) }
    50% { transform: translateX(-5px) }
    75% { transform: translateX(5px) }
    100% { transform: translateX(0) }
}

@media screen and (max-width: 1000px) {
    .game > #grid {
        transform: scale(0.8);
    }
}

@media screen and (max-width: 740px) {
    .game > #grid {
        transform: scale(0.7);
    }
}

@media screen and (max-width: 640px) {
    .game > #grid {
        transform: scale(0.6);
    }
}


@media screen and (max-width: 560px) {
    .game > #grid {
        transform: scale(0.5);
    }
}

@media screen and (max-width: 440px) {
    .game > #grid {
        transform: scale(0.4);
    }
}

@media screen and (max-width: 550px) {
    .pre-game > .main-content > .pill-choice > .pills {
        gap: 60px;
    }
}
</style>