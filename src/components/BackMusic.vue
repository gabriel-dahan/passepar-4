<script setup lang="ts">
const playAudio = () => {
    const audioElem = <HTMLAudioElement>document.getElementById('backsong');
    const btn = <HTMLButtonElement>document.getElementById('songBtn');
    if(!audioElem.paused) {
        audioElem.pause();
        btn.classList.remove('playing');
    }
    else {
        audioElem.play();
        btn.classList.add('playing');
    }
};
</script>

<template>
    <button id="songBtn" @click="playAudio">♪</button>
    <audio id="backsong" loop>
        <source src="@/assets/backsong.mp3">
    </audio>
</template>

<style scoped>

button {
    z-index: 1;
    position: absolute;
    left: 20px;
    bottom: 20px;
    outline: none;
    border: 2px transparent solid;
    border-radius: 5px;
    transition: 0.3s;
    background-color: gray;
    font-size: 16px;
}

button:hover {
    background-color: #1ec572;
}

button.playing:not(:hover) {
    background: #31f593;
}
</style>