<script setup lang="ts">
import { Connect4API } from '@/assets/ts/api';
import { ref } from 'vue';
import Form from '@/components/Form.vue';

const username = ref('');
const email = ref('');
const pwd = ref('');
const confPwd = ref('');

const errors = ref({
    p1: { // Email or username already exists
        1: false,
        2: false
    }, 
    p3: false // Email is not valid
})

const createUser = (e: Event) => {
    if (pwd.value == confPwd.value)
        Connect4API.players.register(username.value, email.value, pwd.value)
            .then(data => {
                if(data?.code == 'P3') {
                    errors.value.p3 = true;
                    // (errors.value.p1 as any)[data.subcode] = true;
                    console.log(errors.value)
                }
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
            </div>
            <div class="f-field">
                <label for="email">Email</label>
                <input id="email" type="email" placeholder="passe@par4.fr"
                    v-model="email">
                <span class="field-error" v-if="errors.p3">Cette adresse email n'est pas valide</span>
            </div>
            <div class="f-field">
                <label for="password">Mot de passe</label>
                <input id="password" type="password" placeholder="1234?"
                    v-model="pwd">
            </div>
            <div class="f-field">
                <label for="confirm-password">Confirmer le mot de passe</label>
                <input id="confirm-password" type="password" placeholder="1234!"
                    v-model="confPwd">
            </div>
        </div>
        <div class="f-submit">
            <input type="submit" value="Valider">
        </div>
    </Form>
</template>
