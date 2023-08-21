<template>
    <div class="flex">
        <!-- Sidebar -->
        <div
            :class="['bg-gray-800 p-4', isCollapsed ? 'w-20' : 'w-64']"
            @click="toggleSidebar">
            <button class="mb-4 text-white">Toggle</button>

            <!-- Place your sidebar content here -->
            <div v-if="!isCollapsed">
                <!-- Sidebar details -->
            </div>
        </div>

        <!-- Main Content -->
        <div class="flex-grow">
            <!-- Your main content goes here -->
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
    name: 'MediaPosterEditor',

    setup() {
        const isCollapsed = ref(false);

        const toggleSidebar = () => {
            isCollapsed.value = !isCollapsed.value;
        };

        return {
            isCollapsed,
            toggleSidebar,
        };
    },
});
</script>

<style scoped>
/* You can modify styles as per your needs */
</style>
