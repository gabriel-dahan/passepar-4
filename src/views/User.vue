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
        <div class="center">
            <img class="rounded-card" :src="currentUser.avatar_url" alt="User">

            <p>Utilisateur <span class="username">{{ user.name }}</span> <small>(#{{ user.id }})</small></p>
            <p>Score : <span class="score">{{ user.score }}</span></p>
            <div class="btns">
                <button @click="disconnectUser" v-if="currentUser && currentUser.id === user.id">Se déconnecter</button>
            </div>


        </div>
    </div>
</template>

<style scoped>
.flex-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 30px;
}

.rounded-card {
    border-radius: 50%;

}



.username {
    color: var(--matrix-text);
}


.btns>button {
    margin-top: 5px;
    display: flex;
    gap: 5px;
    font-family: 'Share Tech Mono', cursive;
    padding: 10px 20px;
    border-radius: 8px;
    border-style: solid;
    animation-duration: 4.1s;
    transition-duration: 0.4s;
}

.btns>button {
    border-color: var(--matrix-text);
    background-color: var(--matrix-text);
    gap: 10px;
}

.btns>button:hover {
    background-color: var(--color-background);
    border-color: var(--matrix-text);
    color: var(--matrix-text);
}

.score {
    color: #fff;
}
</style>