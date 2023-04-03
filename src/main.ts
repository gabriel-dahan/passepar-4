import { createApp } from 'vue'
import VueTippy from 'vue-tippy';
import 'tippy.js/dist/tippy.css'

import App from './App.vue'
import './assets/main.css'
import { API } from './assets/ts/api';
import type { User } from './assets/ts/interfaces';

import router from './routes'

const app = createApp(App);
app.use(router);
app.use(VueTippy, {
    defaultProps: { 
        touch: 'hold' 
    },
});
app.mount('#app');

/* Get current logged user (using session token). */
let $promisedUser: Promise<User | null> = Promise.resolve(null);
const sessionToken = localStorage.getItem('auth_token'); // Get auth_token locally stored.
if(sessionToken)
    $promisedUser = API.users.from_session(sessionToken).then(data => { return data?.id ? data : null; });

app.provide('promisedUser', $promisedUser) // Provide global Vue variable to get current user in other vues.

$promisedUser.then(user => {
    router.beforeEach((to, from) => {
        if (to.meta.redirectProfile && user) {
            router.push(`/p/${user.id}`)
        }
    });
});
