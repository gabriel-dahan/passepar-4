import { createApp } from 'vue'

import App from './App.vue'
import './assets/main.css'
import { Connect4API } from './assets/ts/api';
import type { Player } from './assets/ts/interfaces';

import router from './routes'

const app = createApp(App);
app.use(router);
app.mount('#app');

let $promisedUser: Promise<Player | null> = Promise.resolve(null);
const sessionToken = localStorage.getItem('auth_token');
if(sessionToken) {
    $promisedUser = Connect4API.players.from_session(sessionToken).then(data => { return data?.id ? data : null; });
}

app.provide('promisedUser', $promisedUser)

$promisedUser.then(user => {
    router.beforeEach((to, from) => {
        if (to.meta.redirectAuth && user) {
            router.push(`/p/${user.id}`)
        }
    });
});
