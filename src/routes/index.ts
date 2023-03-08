import HomeVue from '@/views/Home.vue'
import LoginVue from '@/views/forms/Login.vue'

import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: HomeVue
        },
        {
            path: '/login',
            component: LoginVue
        }
    ]
})

export default router;