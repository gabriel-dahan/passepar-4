<script setup lang="ts">
const playAudio = () => {
    const audioElem = <HTMLAudioElement>document.getElementById('backsong');
    audioElem.play();
};
</script>

<template>
    <button @click="playAudio">SONG ?</button>
    <audio id="backsong">
        <source src="@/assets/backsong.mp3">
    </audio>
</template>

<style scoped>
audio {
    position: absolute;
    width: 100vw;
    height: 100vh;
}
</style>