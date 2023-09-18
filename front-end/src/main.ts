import { createApp } from 'vue';
import ElementPlus from 'element-plus';

import App from './App.vue';
import { store } from './store';
import { router } from './router';
import PrimeVue from 'primevue/config';
import { updateTheme } from './utils/theme';

import 'uno.css';
import "vue3-colorpicker/style.css";

import '@/assets/styles/tailwind.css';
async function main() {

    const app = createApp(App);

    // load plugins
    app.use(store);
    app.use(router);
    app.use(PrimeVue);
    // app.use(ElementPlus);
    // app.use(i18n);

    app.mount('#app');

    updateTheme();
}

main();
