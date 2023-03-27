<script setup lang="ts">
import { Connect4API } from '@/assets/ts/api';
import { ref, onMounted } from 'vue';
import { APP_NAME } from '@/assets/ts/utils';

let firstGame = ref('');

const newGame = () => {
    Connect4API.games.new(true).catch(err => console.error(err));
}

onMounted(() => {
    Connect4API.games.list().then(data => {
        if(data.games.length !== 0)
            firstGame.value = data.games[0].id
        else {
            Connect4API.games.new(true).then(data => {
                firstGame.value = data.game.id
            });
        }
    });
});
</script>

<template>
    <header>
        <h1>{{ APP_NAME }}</h1>
        <nav>
            <ul>
                <li>
                    <router-link to="/">Home</router-link>
                </li>
                <li>
                    <router-link to="/login">Login</router-link>
                </li>
                <li>
                    <router-link to="/register">Register</router-link>
                </li>
                <li>
                    <router-link :to="'/game/' + firstGame">Example Game</router-link>
                </li>
                <li>
                    <button @click="newGame">New Public Game</button>
                </li>
            </ul>
        </nav>
    </header>
</template>


<style scoped>
header {
    background-color: var(--color-background-soft);
    padding: 1rem;
    display: flex;
    gap: 20px;
}

header > h1 {
    font-size: 17px;
}

header > nav > ul {
    padding: 0;
    list-style: none;
    display: flex;
    gap: 10px;
}

header > nav > ul > li > a {
    color: #2593dd;
    
}
</style>
