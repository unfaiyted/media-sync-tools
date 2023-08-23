<template>
    <div>
        <div
            @dragover.prevent
            @drop="onDrop"
            class="dropzone"
        >
            Drop your files here!
            <input type="file" ref="fileInput" @change="onFileChange" style="display: none" />
        </div>
    </div>
    <div v-if="confirmationMessage" class="confirmation">
            {{ confirmationMessage }}
        </div>

        <img v-if="lastUploadedImageUrl" :src="lastUploadedImageUrl" alt="Last Uploaded Image" width="100" />

        <select v-if="uploadedFiles.length" v-model="selectedFile">
            <option v-for="file in uploadedFiles" :key="file">{{ file }}</option>
        </select>

</template>

<script>
import {API_URL} from "@/utils/constants";

export default {
    data() {
        return {
            confirmationMessage: '',
            lastUploadedImageUrl: '',
            uploadedFiles: [],
            selectedFile: null,
        };
    },
    watch: {
        // lastUploadedImageUrl: "fetchFileList",
        selectedFile: 'updateBackgroundImage'
    },
    methods: {
        // ... rest of the methods
        async onDrop(event) {
            event.preventDefault();
            const file = event.dataTransfer.files[0]; // Assuming only one file is dropped
            this.uploadFile(file);
        },
        updateBackgroundImage() {
            this.$emit("background-image-selected", { backgroundImage: this.selectedFile });
        },
        onFileChange(event) {
            const file = event.target.files[0];
            this.uploadFile(file);
        },

        async uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch(`${API_URL}/poster/background/`, {
                    method: 'POST',
                    body: formData,
                });
                const data = await response.json();
                this.confirmationMessage = `File uploaded: ${data.filename}`;
                this.lastUploadedImageUrl = URL.createObjectURL(file);

            } catch (error) {
                this.confirmationMessage = 'Error uploading the file.';
                console.error("File upload error:", error);
            }
        },

    },
    async created() {
    },
}
</script>


<style>
.dropzone {
    width: 100%;
    height: 200px;
    border: 3px dashed #ccc;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}
</style>
