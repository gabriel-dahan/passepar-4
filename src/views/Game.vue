<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { useRoute } from 'vue-router';

import { Connect4API } from '@/assets/ts/api';
import { matrixAsColumns } from '@/assets/ts/utils';
import LoadingPage from '@/components/LoadingPage.vue';

const route = useRoute();
const id = route.params.id as string;

const data = ref({
    'id': null,
    'matrix': [],
    'players': []
});

const loadGame = () => {
    Connect4API.games.get(id)
        .then(res => {
            res.matrix = matrixAsColumns(res.matrix);
            data.value = res;
        }) // Store returned data to the 'data' variable.
        .catch(error => console.error(error));
}
    
const play = (event: any, column: number) => {
    Connect4API.games.play(id, String(column))
        .then(data => {
            loadGame(); // Reloads the game's data.

            if(data.code && data.code === 'G3') {
                alert(`Column ${column + 1} is full.`) // Testing purposes.
            }
        })
        .catch(error => console.error(error));
};

onBeforeMount(() => {
    loadGame()
});
</script>

<template>
    <div class="pre-game" v-if="data.id && data.players.length < 2">
        <h1 class="game-title">Partie #{{ data.id }}</h1>
        <p class="players-count">Joueurs : {{ data.players.length }}/2</p>
        <p>Choisissez la pilule de votre choix...</p>
        <div class="pill-choice">
            <img src="@/assets/choices_left.png" alt="Red Pill">
            <img src="@/assets/choices_right.png" alt="Blue Pill">
        </div>
    </div>
    <div class="game" v-else-if="data.id && data.players.length === 2">
        <div id="grid">
            <!-- Loop goes from 1 to n (not 0 to n-1 in VueJS !), so we have to substract 1 to the index... -->
            <div :class="'column-' + (index - 1)" @click="$event => play($event, index - 1)" v-for="index in data.matrix.length">
                <div class="cells">
                    <div class="cell" v-for="cell in data.matrix[index - 1]">
                        <img src="@/assets/pawn1.svg" alt="P1" v-if="cell == '1'">
                        <img src="@/assets/pawn2.svg" alt="P2" v-else-if="cell == '2'">
                        <img src="@/assets/void.svg" alt="NP" v-else>
                    </div>
                </div>
                <hr width="90%">
                <span class="col-num">{{ index }}</span>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pre-game,
.game {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.pre-game > .game-title {
    font-family: 'Share Tech Mono', cursive;
    color: var(--matrix-text);
}

.pre-game > p {
    font-family: 'Share Tech Mono', cursive;
}

.pre-game > .pill-choice {
    display: flex;
    justify-content: center;
    gap: 100px;
}

.pre-game > .pill-choice > img {
    height: 150px;
    width: auto;
    transition: transform 0.3s ease-out;
}

.pre-game > .pill-choice > img:hover {
    transform: scale(1.2);
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