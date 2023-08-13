
import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from './views/DashboardView.vue';
import Settings from './views/SettingsView.vue';
import About from './views/AboutView.vue';
import ListView from './views/ListView.vue';
import ToolsView from "@/views/ToolsView";
import PosterView from "@/views/PosterView";

const routes = [
    { path: '/', component: DashboardView },
    { path: '/settings', component: Settings },
    { path: '/about', component: About },
    { path: '/list', component: ListView },
    { path: '/tools', component: ToolsView },
    { path: '/poster', component: PosterView }

];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;
