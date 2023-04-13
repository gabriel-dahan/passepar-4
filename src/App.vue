
<script setup lang="ts">
import NavBar from '@/components/NavBar.vue';
import LoadingPage from '@/components/LoadingPage.vue';
</script>

<script lang="ts">
const inputs = document.getElementsByTagName('input');
Array.from(inputs).forEach(input => {
    input.setAttribute('spellcheck', 'false');
});
</script>

<template>
    <LoadingPage></LoadingPage>
    <NavBar></NavBar>
    <main>
        <router-view />
    </main>
    <!-- <Footer></Footer> -->
</template>