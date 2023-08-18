import { getToken } from '@/utils/token';
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Dashboard from '@/pages/Dashboard.vue'
import Settings from '@/pages/Settings.vue'
import About from '@/pages/About.vue'
import UserLists from '@/pages/UserLists.vue'
import MediaList from '@/pages/List.vue'
import Tools from '@/pages/Tools.vue'
import Poster from '@/pages/Poster.vue'
import Admin from '@/pages/Admin.vue'

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Index',
        meta: {
            title: 'Dashboard Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: Dashboard
    },
    {
        path: '/settings',
        name: 'Settings',
        meta: {
            title: 'Settings Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: Settings,
    },
    {
        path: '/about',
        name: 'About',
        meta: {
            title: 'About Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: About,
    },
     {
         path: '/lists',
         name: 'Lists',
         meta: {
             title: 'List Page',
             keepAlive: true,
             requireAuth: false,
         },
         component: UserLists,
     },
      {
         path: '/list/:listId',
         name: 'List',
         meta: {
             title: 'List Page',
             keepAlive: true,
             requireAuth: false,
         },
         component: MediaList,
     },
     {
         path: '/tools',
         name: 'Tools',
         meta: {
             title: 'Tools Page',
             keepAlive: true,
             requireAuth: false,
         },
         component: Tools,
     },
    {
        path: '/poster',
        name: 'Poster',
        meta: {
            title: 'Poster Page',
            keepAlive: true,
            requireAuth: false,
        },
        component: Poster,
    },
     {
        path: '/admin',
          name: 'Admin',
             meta: {
                 title: 'Admin Page',
                 keepAlive: true,
                 requireAuth: false,
             },
             component: Admin,
     }
];

export default routes;
const router = createRouter({
    history: createWebHistory(),
    routes,
});

// router.beforeEach(async (to, from) => {
//     const token = getToken();
//     if (!token && to.name !== 'Index') {
//         return { name: 'Index' };
//     }
// });

export { router };
