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

onBeforeMount(() => {
    Connect4API.games.get(id)
        .then(res => data.value = res) // Store returned data to the 'data' variable.
        .catch(error => console.error(error));
});
</script>

<template>
    <div class="grid">
        <div class="column" v-for="column in matrixAsColumns(data.matrix)">
            <div class="cell" v-for="cell in column">
                {{ cell }}
            </div>
        </div>
    </div>
    <!-- <pre><code>{{ data }}</code></pre> -->
</template>

<style scoped>
.grid {
    justify-content: center;
    align-items: center;
    display: flex;
}

.grid > .column {
    display: flex;
    flex-direction: column;
    border: 2px rgba(255, 255, 255, 0) solid;
}

.grid > .column:hover {
    border: 2px rgb(113, 113, 219) solid;
}

.grid > .column > .cell {
    padding: 20px 30px;
    border: 1px white solid;
}
</style>