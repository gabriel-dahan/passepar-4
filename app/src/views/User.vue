<script setup lang="ts">
import { inject, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import type { User } from '@/assets/ts/interfaces';
import { loadCurrentUser } from '@/assets/ts/utils';
import { API } from '@/assets/ts/api';

const route = useRoute();
const router = useRouter();
const id = route.params.id as string;
const user = ref({} as User);

const $promisedUser: Promise<User> | Promise<null> | undefined = inject('promisedUser');
const currentUser = ref({} as User | null);

const loadRequestedUser = async () => {
    let u: User = await API.users.get(id);
    if (!u.id)
        alert('Requested user does not exist.');
    else
        user.value = u;
}

const disconnectUser = () => {
    API.users.delete_session(localStorage.getItem('auth_token') as string).then(data => {
        localStorage.removeItem('auth_token');
        router.push('/').then(() => router.go(0));
    })
}

onMounted(async () => {
    await loadCurrentUser($promisedUser, currentUser);
    await loadRequestedUser();
});
</script>

<template>
    <div class="flex-container">
        <img class="rounded-card" :src="user.avatar_url" alt="Avatar">
        <div class="infos">
            <p>Utilisateur <span class="username">{{ user.name }}</span> <span v-if="currentUser?.id === user.id">(vous)</span> <small>(#{{ user.id }})</small></p>
            <p>Score : <span class="score">{{ user.score }}</span></p>
            <div class="btns">
                <button @click="disconnectUser" v-if="currentUser?.id === user.id">Se déconnecter</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.flex-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
}

.rounded-card {
    border-radius: 50%;
    width: 75px;
    height: auto;
}

.username {
    color: var(--matrix-text);
}

.infos {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.btns > button {
    font-family: 'Share Tech Mono', cursive;
    padding: 5px 15px;
    border-radius: 5px;
    border-style: solid;
    transition: 0.3s;
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
}

.btns > button:hover {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.score {
    color: #fff;
}
</style>