
<script setup lang="ts">
import NavBarDesk from '@/components/NavBarDesk.vue';
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
    <NavBarDesk></NavBarDesk>
    <main>
        <router-view />
    </main>
    <!-- <Footer></Footer> -->
</template>