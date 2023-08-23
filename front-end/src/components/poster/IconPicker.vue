<template>
    <div>
        <select v-model="selectedFile">
            <option v-for="file in files" :key="file">{{ file }}</option>
        </select>

    </div>
</template>

<script>
import {API_URL} from "@/utils/constants";

export default {
    data() {
        return {
            files: [],
            selectedFile: null,
        };
    },
    watch: {
        selectedFile: "updateIcon",
    },
    mounted() {
        // Make an API call when the component is mounted
        this.fetchFiles();
    },
    methods: {
        updateIcon() {
            console.log("updateIcon")
            this.$emit("icon-selected", { icon: this.selectedFile });
        },
        async fetchFiles() {
            try {
                // Call our API endpoint (you may need to adjust the URL or add params if needed)
                const response = await fetch(`${API_URL}/icons/filenames`);
                const data = await response.json();
                this.files = data.filenames;
            } catch (error) {
                console.error("Error fetching files:", error);
            }
        },
    },
};
</script>
