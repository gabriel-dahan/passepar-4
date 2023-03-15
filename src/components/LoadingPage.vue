<script setup lang="ts">
import { ref, onMounted } from 'vue';

let isLoading = ref(true);

onMounted(() => {
    isLoading.value = false;
});
</script>

<template>
    <div class="page-load" v-if="isLoading === true">
        <h1 color="white">HELLO</h1>
    </div>
</template>

<style scoped>
.page-load {
    z-index: 1000;
    position: absolute;
    background-color: black;
    width: 100%;
    height: 100%;
}
.page-load > h1 {
    left: 50%;
}
</style>