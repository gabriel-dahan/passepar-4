<script setup lang="ts">
import { onMounted } from 'vue';

onMounted(() => {
    const customCursor = document.getElementById('cursor') as HTMLDivElement;

    document.addEventListener('mousemove', (e) => {
        let x = e.clientX;
        let y = e.clientY;

        customCursor.style.left = `${x}px`;
        customCursor.style.top = `${y}px`;
    });
})
</script>

<template>
    <div id="cursor">
        <!-- <img src="@/assets/cursor.png" alt=""> -->
    </div>
</template>

<style scoped>
#cursor {
    z-index: 1000;
    position: fixed;
    width: 10px;
    height: 10px;
    transform: translate(-50%, -50%);
    background-color: rgb(50, 238, 91);
    /* mix-blend-mode: difference; */
    border-radius: 50%;
    pointer-events: none;
    transition: width 0.5s, height 0.5s;
}

/* In case we need an image as a cursor...
#cursor > img {
    width: 15px;
    height: 15px;
    position: relative;
    left: -2px;
    top: -5px;
} */
</style>