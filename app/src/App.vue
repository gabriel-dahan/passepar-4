
<script setup lang="ts">
import NavBar from '@/components/NavBar.vue';
</script>

<script lang="ts">
const inputs = document.getElementsByTagName('input');
Array.from(inputs).forEach(input => {
    input.setAttribute('spellcheck', 'false');
});
</script>

<template>
    <NavBar></NavBar>
    <main>
        <router-view />
    </main>
</template>