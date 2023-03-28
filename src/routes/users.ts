import LoginVue from '@/views/forms/Login.vue';
import RegisterVue from '@/views/forms/Register.vue';
import UserVue from '@/views/User.vue';

export default [
    {
        path: '/login',
        component: LoginVue,
        meta: { redirectProfile: true }
    },
    {
        path: '/register',
        component: RegisterVue,
        meta: { redirectProfile: true }
    },
    {
        path: '/p/:id',
        component: UserVue
    }
];