<template>
    <div class="library-config">
        <h2>Add New Library</h2>
        <form @submit.prevent="addLibrary">
            <div>
                <label for="libraryName">Library Name</label>
                <input v-model="newLibrary.name" id="libraryName" type="text" required />
            </div>
            <div>
                <label for="libraryType">Library Type</label>
                <input v-model="newLibrary.type" id="libraryType" type="text" required />
            </div>
            <div>
                <label for="clientName">Client Name</label>
                <input v-model="newLibrary.client_name" id="clientName" type="text" required />
            </div>
            <div>
                <label for="clientType">Client Type</label>
                <input v-model="newLibrary.client_type" id="clientType" type="text" required />
            </div>
            <button type="submit">Add Library</button>
        </form>
        <h2>Libraries</h2>
        <ul>
            <li v-for="library in libraries" :key="library.id">
                <span>{{ library.name }}</span>
                <button @click="deleteLibrary(library.id)">Delete</button>
            </li>
        </ul>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    data() {
        return {
            newLibrary: {
                name: '',
                type: '',
                client_name: '',
                client_type: '',
            },
            libraries: [],
        };
    },
    methods: {
        generateGuid() {
            // Implementation for generating GUID
        },
        async addLibrary() {
            const newLibrary = {
                id: this.generateGuid(),
                name: this.newLibrary.name,
                clients_to_sync: [
                    {
                        id: this.generateGuid(),
                        name: this.newLibrary.client_name,
                        type: this.newLibrary.client_type,
                    },
                ],
                type: this.newLibrary.type,
            };

            // Make an API call to add the newLibrary
            // ...

            // Assuming the API call is successful, update the UI
            this.libraries.push(newLibrary);

            // Reset the form
            this.newLibrary = {
                name: '',
                type: '',
                client_name: '',
                client_type: '',
            };
        },
        async deleteLibrary(libraryId) {
            // Make an API call to delete the library by its ID
            // ...

            // Assuming the API call is successful, update the UI
            this.libraries = this.libraries.filter(library => library.id !== libraryId);
        },
        // You can implement methods for editing and updating libraries here
    },
});
</script>
