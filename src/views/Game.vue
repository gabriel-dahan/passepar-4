<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import { Connect4API } from '@/assets/ts/api';

const route = useRoute();
const id = route.params.id as string;

const data = ref(null);

onMounted(() => {
    Connect4API.games.get(id)
        .then(res => data.value = res)
        .catch(error => console.error(error));
});
</script>

<template>
    <pre><code>{{ data }}</code></pre>
</template>