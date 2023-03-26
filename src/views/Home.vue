<script setup lang="ts">
import { ref, type ComponentPublicInstance } from 'vue';

import { APP_NAME } from '@/assets/ts/utils';
import { Connect4API } from '@/assets/ts/api';

let gameId = ref('');

// Err. codes
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
    <div class="centered">
        <div class="content">
            <h2 class="write-code">Entrez un code :</h2>
            <input v-model="gameId" placeholder="ex. : 4q04h92">
            <p v-if="G2">Game with ID '{{ gameId }}' doesn't exist :(</p>
            <div class="btns">
                <button type="submit" @click="$event => getGame">Go !</button>
                <button type="button">login/sign up</button>
            </div>
            <p><u>Vous devez avoir un compte afin de créer une partie.</u></p> <br>
            <p>Bienvenue sur cette réplique du fameux jeu <u>Puissance 4</u>, connu pour sa simplicité, sans prise de tête. <br>
            Ici, on préfère la prise de tête, raison pour laquelle on introduit avec cette reproduction un système compétitif, où celui gagnant le plus de 
            parties et obtenant le plus de points sera l'élu du classement !</p>
            <h2>Parties publiques : </h2>
        </div>
    </div>
</template>

<style scoped>
p {
    font-family: 'Share Tech Mono', cursive;
    text-align: center;
}

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

h2 {
    padding-bottom: 20px;
}

.centered {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.centered > .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    max-width: 550px;
}

.content > input {
    outline: none;
    padding: 5px;
    border: 1px var(--matrix-text) solid;
    border-radius: 5px;
    font-family: 'Share Tech Mono', cursive;
    font-size: 16px;
    color: var(--text-color);
    background-color: rgb(31, 31, 31);
}

.content > ::placeholder {
    font-family: 'Share Tech Mono', cursive;
    color: var(--text-color);
}

.content h2 {
    color: var(--matrix-text);
    font-family: 'Share Tech Mono', cursive;
    text-align: center;
}

.content > .write-code {
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
    font-family: 'Share Tech Mono';
    animation-duration: 4.1s;
    transition-duration: 0.4s;
}

.content > .btns > button[type='submit'] {
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
}

.content > .btns > button[type='submit']:hover {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.content > .btns > button[type='button'] {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.content > .btns > button[type='button']:hover {
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
    color: #000;
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