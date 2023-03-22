<script setup lang="ts">
import { ref, type ComponentPublicInstance } from 'vue';

import { APP_NAME } from '@/assets/ts/utils';
import { Connect4API } from '@/assets/ts/api';

let gameId = ref('');

let G2 = ref(false);

const getGame = (vm: ComponentPublicInstance) => {
    const gId = gameId.value;
    Connect4API.games.get(gId).then(data => {
        if (data.code !== 'G2')
            vm.$router.push({ name: 'game', params: { gId } });
        else
            G2.value = true;
    });
}
</script>

<template>
    <h1>{{ APP_NAME }}</h1>
    <div class="content">
        <h2>Entrez le code :</h2>
        <input v-model="gameId" placeholder="ex. : 4q04h92">
        <p v-if="G2">Game with ID '{{ gameId }}' doesn't exist :(</p>
        <div class="btns">
            <button type="submit" @click="$event => getGame">Go !</button>
            <button type="button">login/sign up</button>
        </div>
    </div>
</template>

<style scoped>
h1 {
    font-family: 'Press Start 2P', cursive;
    color: var(--matrix-text);
    text-align: center;
    margin-top: 1rem;
    margin-bottom: 3rem;
    animation-duration: .8s;
    animation-name: blinking;
    animation-iteration-count: infinite;
    transition: none;
}

.content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.content > input {
    outline: none;
    padding: 5px;
    border: 1px var(--matrix-text) solid;
    border-radius: 5px;
    font-family: 'Share Tech Mono', cursive;
    color: var(--text-color);
    background-color: rgb(31, 31, 31);
}

.content > ::placeholder {
    font-family: 'Share Tech Mono', cursive;
    color: var(--text-color);
}

.content > h2 {
    color: var(--matrix-text);
    font-family: 'Share Tech Mono', cursive;
    overflow: hidden;
    white-space: nowrap;
    width: 16ch;
    animation: typing 4s steps(16, end);
}

.content > input[type=text] {
    background-color: var(--color-background);
    opacity: 0;
    color: var(--matrix-text);
    font-family: 'Share Tech Mono', cursive;
    outline: none;
}

.content > .btns {
    display: flex;
    gap: 5px;
}

.content > .btns > button {
    padding: 10px 20px;
    border-radius: 8px;
    border-style: solid;
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
    font-family: 'Share Tech Mono';
    animation-duration: 4.1s;
    transition-duration: 0.4s;
}

.content > .btns > button:hover {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

/* ANIMATIONS */

@keyframes typing {
    0% { width: 0; }
}

@keyframes blinking {
    0% {
        opacity: 1;
    }

    40% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}
</style>