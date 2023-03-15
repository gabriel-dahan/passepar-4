
<script setup lang="ts">
import { onMounted, ref } from 'vue';

import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';

let isLoading = ref(true);

onMounted(() => {
    isLoading.value = false;
});
</script>

<template>
    <div class="page-load" v-if="isLoading === true">
        <h1 color="white">HELLO</h1>
    </div>
    <Header></Header>
    <main>
        <router-view />
    </main>
    <Footer></Footer>
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