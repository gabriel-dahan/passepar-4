<script setup lang="ts">
import { inject, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const id = route.params.id as string;

const $promisedUser = inject('promisedUser');
const isAuthenticated = ref($promisedUser !== Promise.resolve(null));

const disconnectUser = () => {
    localStorage.removeItem('auth_token');
    router.push('/').then(() => router.go(0));
}
</script>

<template>
    <p>User {{ id }}</p>
    <button @click="disconnectUser" v-if="isAuthenticated">Se déconnecter</button>
</template>

<style scoped></style>