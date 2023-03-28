<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { API, getRawErrs, updateErrs } from '@/assets/ts/api';
import Form from '@/components/Form.vue'

const router = useRouter();

/* --- REFS --- */
const email = ref('');
const pwd = ref('');

const errors = ref(getRawErrs());
/* ------------ */

const logUser = (e: SubmitEvent) => {
    API.users.login(email.value, pwd.value)
        .then(data => {
            errors.value = getRawErrs();
            if(data.auth_token) {
                localStorage.setItem('auth_token', data.auth_token)
                router.push(`/p/${data.user.id}`).then(() => router.go(0));
            }
            else if(data && data.code)
                updateErrs(errors, data);
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
                <span class="f-error" v-if="errors.U2">Cette adresse email n'est pas enregistrée.</span>
            </div>
            <div class="f-field">
                <label for="password">Mot de passe</label>
                <input id="password" type="password" placeholder="1234?"
                    v-model="pwd">
                <span class="f-error" v-if="errors.U4">Le mot de passe entré est incorrect.</span>
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