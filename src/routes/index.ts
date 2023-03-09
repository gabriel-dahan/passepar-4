import { createRouter, createWebHistory } from 'vue-router'

import HomeVue from '@/views/Home.vue'

import userRoutes from './users'
import gameRoutes from './games'

export default createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: HomeVue
        },
    ].concat(
        userRoutes, 
        gameRoutes
    )
});