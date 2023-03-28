<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

import { API, getRawErrs, updateErrs } from '@/assets/ts/api';
import Form from '@/components/Form.vue';

const router = useRouter();

/* --- REFS --- */
const username = ref('');
const email = ref('');
const pwd = ref('');
const confPwd = ref('');

const errors = ref({
    ...getRawErrs(),
    noMatch: false
});
/* ------------ */

const pwdMatch = (e: KeyboardEvent) => {
    if(pwd.value == confPwd.value)
        errors.value.noMatch = false;
    else
        errors.value.noMatch = true;
}

const createUser = (e: SubmitEvent) => {
    if (pwd.value == confPwd.value && pwd.value !== '' && confPwd.value !== '')
        API.users.register(username.value, email.value, pwd.value)
            .then(data => {
                errors.value = {
                    ...getRawErrs(),
                    noMatch: false
                };
                if(data?.user)
                    router.push('/login')
                else if(data && data.code)
                    updateErrs(errors, data);
            });
}
</script>

<template>
    <Form @submited="createUser">
        <h2>S'enregistrer</h2>
        <div class="fields" >
            <div class="f-field">
                <label for="username">Nom d'utilisateur</label>
                <input id="username" type="text" placeholder="PassePar4"
                    v-model="username">
                <span class="f-error" v-if="errors.U1.S2">Ce nom est déjà utilisé.</span>
            </div>
            <div class="f-field">
                <label for="email">Email</label>
                <input id="email" type="email" placeholder="passe@par4.fr"
                    v-model="email">
                    <span class="f-error" v-if="errors.U1.S1">Cette adresse mail est déjà utilisée.</span>
                <span class="f-error" v-if="errors.U3">Cette adresse email n'est pas valide</span>
            </div>
            <div class="f-field">
                <label for="password">Mot de passe</label>
                <input id="password" type="password" placeholder="1234?"
                    @keyup="pwdMatch"
                    v-model="pwd">
            </div>
            <div class="f-field">
                <label for="confirm-password">Confirmer le mot de passe</label>
                <input id="confirm-password" type="password" placeholder="1234!" 
                    @keyup="pwdMatch"
                    v-model="confPwd">
                <span class="f-error" v-if="errors.noMatch">Les mots de passe ne correspondent pas.</span>
            </div>
        </div>
        <div class="f-submit">
            <input type="submit" value="Valider">
        </div>
        <p class="have-an-acc">Vous avez déjà un compte ? <router-link to="/login">Se connecter</router-link></p>
    </Form>
</template>

<style scoped>
.have-an-acc > a {
    text-decoration: none;
    color: var(--link-blue);  
}

.have-an-acc > a:hover {
    color: var(--link-blue-hover);
}
</style>
