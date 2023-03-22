
<script setup lang="ts">
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
import LoadingPage from './components/LoadingPage.vue';
import Cursor from './components/Cursor.vue';
</script>

<template>
    <LoadingPage></LoadingPage>
    <Cursor></Cursor>
    <Header></Header>
    <main>
        <router-view />
    </main>
    <!-- <Footer></Footer> -->
</template>