<script setup lang="ts">
import { inject, ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import type { User } from '@/assets/ts/interfaces';
import { loadCurrentUser } from '@/assets/ts/utils';

const route = useRoute();
const router = useRouter();
const id = route.params.id as string;

const $promisedUser: Promise<User> | Promise<null> | undefined = inject('promisedUser');
const currentUser = ref({} as User | null);

const disconnectUser = () => {
    localStorage.removeItem('auth_token');
    router.push('/').then(() => router.go(0));
}

onMounted(async () => {
    await loadCurrentUser($promisedUser, currentUser);
});
</script>

<template>
    <p>User {{ id }}</p>
    <button @click="disconnectUser" v-if="currentUser && currentUser.id === id">Se déconnecter</button>
</template>

<style scoped></style>