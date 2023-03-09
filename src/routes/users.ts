import LoginVue from '@/views/forms/Login.vue'
import RegisterVue from '@/views/forms/Register.vue'

export default [
    {
        path: '/login',
        component: LoginVue,
        meta: {
            /* A modifier : condition vraie ssi le joueur est actuellement connecté. 
                -- Renverra sur la page d'accueil si c'est le cas. */
            logged: false 
        }
    },
    {
        path: '/register',
        component: RegisterVue
    }
];