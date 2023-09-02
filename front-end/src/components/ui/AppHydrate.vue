<template>
    <div>
        <div v-if="loading">
            Loading configuration...
        </div>
        <div v-if="error">
            An error occurred: {{ errorMessage }}
        </div>
        <div v-if="!loading">
            <!-- Display hydrated data as needed or pass it to child components -->
            <slot></slot>
        </div>
    </div>
</template>

<script type="ts">
import axios from 'axios';
import {hydrateApp} from "@/api/configs";
import { useAppConfigStore} from "@/store/appConfigStore";

export default {
    name: 'AppHydrate',
    data() {
        return {
            appConfig: null,
            loading: true,
            error: false,
            errorMessage: '',
        };
    },
    methods: {
        async hydrateApp() {
            const store = useAppConfigStore();
            try {
                const userId = 'APP-DEFAULT-USER'; // You'd retrieve this from somewhere in your app, e.g., user authentication
                console.log('Hydrating app for user', userId);
                store.appConfig = await store.hydrateApp(userId)
                this.appConfig = store.appConfig;
                console.log(this.appConfig)
            } catch (err) {
                this.error = true;
                this.errorMessage = err.response ? err.response.data.detail : 'An unexpected error occurred';
            } finally {
                this.loading = false;
            }
        }
    },
    created() {
        this.hydrateApp();
    }
};
</script>

<style scoped>
/* Add your styles here */
</style>
