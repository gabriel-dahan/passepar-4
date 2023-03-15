<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { useRoute } from 'vue-router';

import { Connect4API } from '@/assets/ts/api';
import { matrixAsColumns } from '@/assets/ts/utils';

const route = useRoute();
const id = route.params.id as string;

const data = ref({
    'matrix': []
});

const loadGame = () => {
    Connect4API.games.get(id)
        .then(res => {
            res.matrix = matrixAsColumns(res.matrix);
            data.value = res;
        }) // Store returned data to the 'data' variable.
        .catch(error => console.error(error));
}
    
onBeforeMount(() => {
    loadGame()
});
    
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
</script>

<template>
    <div class="pill-choice">
        <img src="@/assets/choices_left.png" alt="Red Pill">
        <img src="@/assets/choices_right.png" alt="Blue Pill">
    </div>
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
</template>

<style scoped>
.pill-choice {
    display: flex;
    justify-content: center;
    gap: 30px;
}

.pill-choice > img {
    height: 100px;
    width: auto;
}

#grid {
    justify-content: center;
    align-items: center;
    display: flex;
}

#grid > [class^='column-'] {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 5px;
}

#grid > [class^='column-'] > .col-num {
    font-family: 'VT323', monospace;
    font-size: 18px;
}

#grid > [class^='column-'] > .cells {
    display: flex;
    flex-direction: column;
    border: 2px transparent solid;
    border-radius: 5px;
}

#grid > [class^='column-']:hover > .cells {
    border: 2px var(--color-text) /*rgb(50, 238, 91) rgb(113, 113, 219) */ solid;
}


#grid > [class^='column-'] > .cells > .cell {
    padding: 20px 30px;
}

#grid > [class^='column-'] > .cells > .cell > img {
    user-select: none;
    -webkit-user-select: none;
    -ms-user-select: none;
    width: 50px;
    height: auto;
    rotate: -30deg;
}
</style>