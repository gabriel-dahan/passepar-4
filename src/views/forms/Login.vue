<script setup lang="ts">
import Form from '@/components/Form.vue'
</script>

<template>
    <Form>
        <label for="email">Email</label> <br>
        <input id="email" type="email"> <br>

        <label for="password">Mot de passe</label> <br>
        <input id="password" type="password"> <br>

        <input type="submit" value="Se connecter">
    </Form>
</template>
