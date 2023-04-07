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
    if(!u.id)
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
    <p>User {{ user.id }} - {{ user.name }}</p>
    <button @click="disconnectUser" v-if="currentUser && currentUser.id === user.id">Se déconnecter</button>
</template>

<style scoped></style>