<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Connect4API } from '@/assets/ts/api';
import Form from '@/components/Form.vue'

const email = ref('');
const pwd = ref('');

const router = useRouter();

const logUser = (e: SubmitEvent) => {
    Connect4API.players.login(email.value, pwd.value)
        .then(data => {
            if(data.auth_token) {
                localStorage.setItem('auth_token', data.auth_token)
                router.push(`/p/${data.player.id}`).then(() => router.go(0));
            }
        });
}
</script>

<template>
    <Form @submited="logUser">
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
        <p class="have-no-acc">Vous n'avez pas de compte ? <router-link to="/register">S'enregistrer</router-link></p>
    </Form>
</template>

<style scoped>
.have-no-acc > a {
    text-decoration: none;
    color: var(--link-blue);  
}

.have-no-acc > a:hover {
    color: var(--link-blue-hover);
}
</style>