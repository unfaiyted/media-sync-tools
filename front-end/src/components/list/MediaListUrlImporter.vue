<template>
    <div class="p-4">
        <div class="mb-4">
            <label for="url" class="block text-sm font-medium text-gray-700">URL</label>
            <input
                type="text"
                id="url"
                v-model="url"
                class="mt-1 p-2 w-full border rounded-md"
                placeholder="Enter media list URL" />
        </div>

        <button
            @click="importList"
            class="bg-blue-600 text-white px-4 py-2 rounded-md"
        >
            Import
        </button>

        <div v-if="listStore.loading" class="mt-2">Loading...</div>
        <div v-if="listStore.error" class="mt-2 text-red-600">{{ listStore.errorMessage }}</div>
    </div>
</template>
<script lang="ts">
import { defineComponent, ref } from "vue";
import { useListStore } from "@/store/listStore";

export default defineComponent({
    name: "MediaListUrlImporter",
    setup() {
        const listStore = useListStore();
        const url = ref("");

        const importList = async () => {
            await listStore.importListFromUrl(url.value);
            if (listStore.error) {
                console.error("Error importing list:", listStore.errorMessage);
            }
        };

        return { url, listStore, importList };
    },
});
</script>

<style scoped>
/* Specific styles for this component can be added here */
</style>
