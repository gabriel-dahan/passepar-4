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
    <div class="playBtn">
        <tippy placement="right" interactive>
            <button id="songBtn" @click="playAudio">♪</button>
            <template #content>
                <p style="width: max-content;">
                    Crédits : 
                    <a href="https://youtu.be/2-wKcIkElIc" target="_blank" style="color: var(--link-blue);">
                        White Bat Audio<img src="@/assets/external-link.svg" alt="" width="13">
                    </a>
                </p>
            </template>
        </tippy>
    </div>
    <audio id="backsong" loop>
        <source src="@/assets/backsong.mp3">
    </audio>
</template>

<style scoped>

.playBtn {
    z-index: 1;
    position: fixed;
    left: 20px;
    bottom: 20px;
}

button {
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