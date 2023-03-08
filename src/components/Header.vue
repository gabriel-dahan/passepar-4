<script setup lang="ts">
</script>

<template>
    <header>
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
            </ul>
        </nav>
    </header>
</template>


<style scoped>
header {
    background-color: var(--color-background-soft);
    padding: 1rem;
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
