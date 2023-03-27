import LoginVue from '@/views/forms/Login.vue';
import RegisterVue from '@/views/forms/Register.vue';
import PlayerVue from '@/views/Player.vue';

export default [
    {
        path: '/login',
        component: LoginVue,
        meta: { redirectAuth: true }
    },
    {
        path: '/register',
        component: RegisterVue,
        meta: { redirectAuth: true }
    },
    {
        path: '/p/:id',
        component: PlayerVue
    }
];