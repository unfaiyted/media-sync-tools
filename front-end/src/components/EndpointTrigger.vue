<template>
    <div>
        <button v-for="endpoint in endpoints" :key="endpoint.name" :class="['btn', loadingEndpoint === endpoint.name ? 'loading' : '']" @click="triggerEndpoint(endpoint.name)">
            {{ endpoint.label }}
            <span v-if="loadingEndpoint === endpoint.name" class="spinner"></span>
        </button>
        <p v-if="responseMessage">{{ responseMessage }}</p>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    name: 'EndpointTrigger',
    setup() {
        const responseMessage = ref('');
        const loadingEndpoint = ref('');  // This will store the endpoint name currently being processed

        const endpoints = [
            { name: 'sync/watchlist', label: 'Sync Watchlist' },
            { name: 'sync/playlist', label: 'Sync Playlist' },
            { name: 'sync/top-lists', label: 'Sync Top Lists' },
            { name: 'sync/collections', label: 'Sync Collections' },
            { name: 'examples', label: 'Trigger Examples' },
            // Note: We may want to handle the webhook differently since it's a POST request
            // { name: 'webhook', label: 'Handle Webhook' },
            { name: 'recommendations', label: 'Get Recommendations' },
            { name: 'sync/trakt', label: 'Sync Trakt' },
            { name: 'sync/config', label: 'Handle Config' },
            { name: 'healthcheck', label: 'Health Check' },
        ];


        const triggerEndpoint = async (endpoint) => {
            loadingEndpoint.value = endpoint;
            try {
                let response = await fetch(`http://localhost:8000/${endpoint}`);
                let data = await response.json();
                responseMessage.value = data.message;
            } catch (error) {
                responseMessage.value = 'Error occurred: ' + error.message;
            } finally {
                loadingEndpoint.value = '';  // Reset the loading indicator for the button
            }
        };

        return {
            responseMessage,
            triggerEndpoint,
            endpoints,
            loadingEndpoint
        };
    },
};
</script>

<style scoped>
.btn {
    padding: 10px 20px;
    margin: 5px;
    border: none;
    border-radius: 5px;
    background-color: #007BFF;
    color: #fff;
    cursor: pointer;
    position: relative;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #0056b3;
}

.btn.loading {
    pointer-events: none;  /* Disable interactions with the button while loading */
}

.spinner {
    border: 2px solid #f3f3f3;
    border-top: 2px solid #fff;
    border-radius: 50%;
    width: 12px;
    height: 12px;
    animation: spin 0.8s linear infinite;
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
}

@keyframes spin {
    0% { transform: translateY(-50%) rotate(0deg); }
    100% { transform: translateY(-50%) rotate(360deg); }
}
</style>
