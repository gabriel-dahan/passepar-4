<script setup lang="ts">
import Form from '@/components/Form.vue'
</script>

<template>
    <Form>
        <label for="username">Nom d'utilisateur</label> <br>
        <input id="username" type="text"> <br>

        <label for="email">Email</label> <br>
        <input id="email" type="email"> <br>

        <label for="password">Mot de passe</label> <br>
        <input id="password" type="password"> <br>

        <label for="confirm-password">Confirmer le mot de passe</label> <br>
        <input id="confirm-password" type="password"> <br>
    </Form>
</template>
