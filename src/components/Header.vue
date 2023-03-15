<script setup lang="ts">
</script>

<template>
    <header>
        <h1>PassPar4</h1>
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
                    <router-link to="/game/4q04h92">Example Game</router-link>
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
