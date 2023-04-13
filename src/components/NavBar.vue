<script setup lang="ts">
import { inject, onMounted, ref } from 'vue';
import BackMusic from '@/components/BackMusic.vue';

import type { User } from '@/assets/ts/interfaces';
import { loadCurrentUser } from '@/assets/ts/utils';

const $promisedUser: Promise<User> | Promise<null> | undefined = inject('promisedUser');
const currentUser = ref({} as User);

onMounted(async () => {
    await loadCurrentUser($promisedUser, currentUser);
});
</script>

<template>
    <nav>
        <ul>
            <li>
                <router-link to="/" v-tippy="{ content: 'Accueil', placement: 'right', theme: 'light' }">
                    <img src="@/assets/icons/home.svg" alt="Home">
                </router-link>
            </li>
            <li>
                <router-link to="/rankings" v-tippy="{ content: 'Classement', placement: 'right', theme: 'light' }">
                    <img src="@/assets/icons/ranking.svg" alt="Rankings">
                </router-link>
            </li>
            <li>
                <router-link to="/search" v-tippy="{ content: 'Rechercher', placement: 'right', theme: 'light' }">
                    <img src="@/assets/icons/search.svg" alt="Search">
                </router-link>
            </li>
            <li class="__blank"></li>
            <li v-if="!currentUser">
                <router-link to="/login" v-tippy="{ content: 'Se connecter', placement: 'right', theme: 'light' }">
                    <img src="@/assets/icons/login.svg" alt="Login">
                </router-link>
            </li>
            <li v-if="currentUser">
                <router-link :to="`/p/${currentUser.id}`" v-tippy="{ content: `Profil - ${currentUser.name}`, placement: 'right', theme: 'light' }">
                    <img class="profile" :src="currentUser.avatar_url" alt="User">
                </router-link>
            </li>
            <li>
                <BackMusic></BackMusic>
            </li>
        </ul>
    </nav>
</template>


<style scoped>
nav {
    z-index: 1000;
    position: fixed;
    height: 100vh;
    width: 75px;
    background-color: var(--color-background-darker);
    border-right: 2px solid var(--matrix-text);
    padding: 30px 0;
}

nav > ul {
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 20px;
    align-items: center;
    list-style: none;
    padding-left: 0;
}

nav > ul > li > a {
    display: flex;
}

nav > ul > li img {
    width: 25px;
    height: auto;
}

nav > ul > li .profile {
    border-radius: 50%;
}

@media screen and (max-width: 900px) {
    nav {
        position: relative;
        width: 100vw;
        height: 60px;
        flex-shrink: 0;
        border-right: none;
        border-bottom: 2px solid var(--matrix-text);
        padding: 0 30px;
    }

    nav > ul {
        flex-direction: row;
    }
}
</style>
