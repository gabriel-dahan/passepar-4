<script setup lang="ts">

import { API } from '@/assets/ts/api';
import type { User } from '@/assets/ts/interfaces';
import { ref, onMounted } from 'vue';

// ---- REFS ---- //

const users = ref([] as User[])

// -------------- //

const loadUsers = async () => {
    API.users.all().then(usersList => {
        users.value = usersList;
    });
};

onMounted(async () => {
    await loadUsers()
});


</script>

<template>
    <div class="rankings">
        <h2>Classement</h2>
        <p>Qui dominera le haut de ce classement ?</p>
        <ul class="ranks">
            <li 
                class="user" 
                v-for="(user, i) in users"
            >
                <img class="crown" src="@/assets/icons/win1.svg" alt="#1" v-if="i == 0">
                <img class="crown" src="@/assets/icons/win2.svg" alt="#2" v-else-if="i == 1">
                <img class="crown" src="@/assets/icons/win3.svg" alt="#3" v-else-if="i == 2">
                <p v-else>#{{ i + 1 }}</p>
                <p>|</p> 
                <img class="avatar" :src="user.avatar_url" alt="Avatar">
                <router-link :to="`/p/${user.id}`"><p>{{ user.name }}</p></router-link>
                <div class="__blank"></div>
                <p style="color: var(--matrix-text)">{{ user.score }}</p>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.rankings {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 50px;
}

.rankings > h2 {
    color: var(--matrix-text);
}

.rankings > ul.ranks {
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 0;
    width: 990px;
}

.rankings > ul.ranks > li.user {
    display: flex;
    gap: 10px;
    align-items: center;
    padding: 5px 10px;
    border-radius: 5px;
    background: var(--color-background-darker);
}

.rankings > ul.ranks > li.user > .crown {
    width: 15px;
    height: auto;
}

.rankings > ul.ranks > li.user > .avatar {
    border-radius: 50%;
    width: 20px;
    height: auto;
}
 
@media screen and (max-width: 1250px) {
    .rankings > ul.ranks {
        width: 90%;
    }
}
</style>