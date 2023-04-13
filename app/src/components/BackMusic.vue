<script setup lang="ts">
const playAudio = () => {
    const audioElem = <HTMLAudioElement>document.getElementById('backsong');
    const btn = <HTMLButtonElement>document.getElementById('song-btn');
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
    <div class="play-btn">
        <tippy placement="bottom" interactive>
            <button id="song-btn" @click="playAudio">
                <img src="@/assets/icons/sound.svg" alt="Sound">
            </button>
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
button {
    width: 30px;
    height: 30px;
    outline: none;
    border: 2px transparent solid;
    border-radius: 5px;
    transition: 0.3s;
    background-color: var(--color-background);
    font-size: 16px;
}

button:hover {
    background-color: var(--matrix-text-softer);
}

button.playing:not(:hover) {
    background: var(--matrix-text);
}

button > img {
    width: 12px;
    height: auto;
}
</style>