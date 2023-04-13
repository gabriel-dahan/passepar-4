import { createRouter, createWebHistory } from 'vue-router';

import HomeVue from '@/views/Home.vue';
import SearchVue from '@/views/Search.vue';
import RankingsVue from '@/views/Rankings.vue';

import userRoutes from './users';
import gameRoutes from './games';

export default createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: HomeVue
        },
        {
            path: '/search',
            component: SearchVue
        },
        {
            path: '/rankings',
            component: RankingsVue
        }
    ].concat(
        userRoutes, 
        gameRoutes
    )
});