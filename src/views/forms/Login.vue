<script setup lang="ts">
import Form from '@/components/Form.vue'

const email = '';
const pwd = '';
</script>

<template>
    <Form>
        <h2>Se connecter</h2>
        <div class="fields">
            <div class="f-field">
                <label for="email">Email</label>
                <input id="email" type="email" placeholder="passe@par4.fr"
                    v-model="email">
            </div>
            <div class="f-field">
                <label for="password">Mot de passe</label>
                <input id="password" type="password" placeholder="1234?"
                    v-model="pwd">
            </div>
        </div>
        <div class="f-submit">
            <input type="submit" value="Valider">
        </div>
    </Form>
</template>
