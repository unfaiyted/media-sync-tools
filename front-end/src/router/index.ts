import { getToken } from '@/utils/token';
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Dashboard',
        meta: {
            title: 'Dashboard Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: () => import('@/pages/Dashboard.vue'),
    },
    {
        path: '/settings',
        name: 'Settings',
        meta: {
            title: 'Settings Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: () => import('@/pages/Settings.vue'),
    },
    {
        path: '/about',
        name: 'About',
        meta: {
            title: 'About Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: () => import('@/pages/About.vue'),
    },
    {
        path: '/list',
        name: 'List',
        meta: {
            title: 'List Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: () => import('@/pages/List.vue'),
    },
    {
        path: '/tools',
        name: 'Tools',
        meta: {
            title: 'Tools Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: () => import('@/pages/Tools.vue'),
    },
    {
        path: '/poster',
        name: 'Poster',
        meta: {
            title: 'Poster Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: () => import('@/pages/Poster.vue'),
    },
    {
       path: '/admin',
         name: 'Admin',
            meta: {
                title: 'Admin Page',
                keepAlive: true,
                requireAuth: false,
            },
            component: () => import('@/pages/Admin.vue'),
    }
];

export default routes;
const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from) => {
    const token = getToken();
    if (!token && to.name !== 'Index') {
        return { name: 'Index' };
    }
});

export { router };
