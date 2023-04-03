
<script setup lang="ts">
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import LoadingPage from './components/LoadingPage.vue';
import Cursor from './components/Cursor.vue';
import BackMusic from './components/BackMusic.vue';
</script>

<script lang="ts">
const inputs = document.getElementsByTagName('input');
Array.from(inputs).forEach(input => {
    input.setAttribute('spellcheck', 'false');
});
</script>

<template>
    <LoadingPage></LoadingPage>
    <BackMusic></BackMusic>
    <!--<Cursor></Cursor>-->
    <Header></Header>
    <main>
        <router-view />
    </main>
    <!-- <Footer></Footer> -->
</template>