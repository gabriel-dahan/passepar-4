<script setup lang="ts">
import { Connect4API } from '@/assets/ts/api';
import { ref, type ComponentPublicInstance } from 'vue';
import { useRouter } from 'vue-router';
import Form from '@/components/Form.vue';

const router = useRouter();

const username = ref('');
const email = ref('');
const pwd = ref('');
const confPwd = ref('');

const errors = ref({
    p1: { // Email or username already exists (API - P1)
        '1': false,
        '2': false
    }, 
    p3: false, // Email is not valid (API - P3)
    pwdNoMatch: false // Password Don't Match
});

const pwdMatch = (e: KeyboardEvent) => {
    if(pwd.value == confPwd.value)
        errors.value.pwdNoMatch = false;
    else
        errors.value.pwdNoMatch = true;
}

const createUser = (e: SubmitEvent) => {
    if (pwd.value == confPwd.value && pwd.value !== '' && confPwd.value !== '')
        Connect4API.players.register(username.value, email.value, pwd.value)
            .then(data => {
                errors.value = {
                    p1: {
                        '1': false,
                        '2': false
                    }, 
                    p3: false,
                    pwdNoMatch: false
                };
                if(data?.code == 'P1')
                    {(errors.value.p1 as any)[data.subcode] = true; console.log(errors.value);}
                else if(data?.code == 'P3')
                    errors.value.p3 = true;
                else if(data?.player)
                    router.push('/login')
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
                <span class="f-error" v-if="errors.p1['2']">Ce nom est déjà utilisé.</span>
            </div>
            <div class="f-field">
                <label for="email">Email</label>
                <input id="email" type="email" placeholder="passe@par4.fr"
                    v-model="email">
                    <span class="f-error" v-if="errors.p1['1']">Cette adresse mail est déjà utilisée.</span>
                <span class="f-error" v-if="errors.p3">Cette adresse email n'est pas valide</span>
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
                <span class="f-error" v-if="errors.pwdNoMatch">Les mots de passe ne correspondent pas.</span>
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
