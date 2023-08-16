<template>
    <div class="p-6">
        <!-- Create Client Field -->
        <h2 class="text-lg font-semibold mb-4">Create Client Field</h2>
        <div class="mb-4">
            <input v-model="newField.name" class="input" placeholder="Name">
        </div>
        <div class="mb-4">
            <input v-model="newField.defaultValue" class="input" placeholder="Default Value">
        </div>
        <button @click="createClientField" class="btn btn-primary">Add Client Field</button>

        <!-- List Client Fields -->
        <h2 class="text-lg font-semibold mt-8 mb-4">Client Fields</h2>
        <ul v-if="clientFields.length">
            <li v-for="field in clientFields" :key="field.clientFieldId" class="mb-2">
                {{ field.name }} ({{ field.clientFieldId }}, {{ field.defaultValue }})
                <button @click="openEditModal(field)" class="btn btn-secondary">Edit</button>
                <button @click="deleteClientField(field.clientFieldId)" class="btn btn-danger">Delete</button>
            </li>
        </ul>

        <!-- Update Client Field Modal -->
        <transition name="modal" enter-active-class="transition-opacity ease-out duration-300" leave-active-class="transition-opacity ease-in duration-300">
            <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center">
                <div class="modal-overlay absolute inset-0 bg-gray-900 opacity-75" @click="closeEditModal"></div>
                <div class="modal-container bg-white w-1/2 mx-auto p-6 rounded shadow-lg">
                    <h3 class="text-lg font-semibold mb-4">Edit Client Field</h3>
                    <div class="mb-4">
                        <input v-model="editingField.name" class="input" placeholder="Name">
                    </div>
                    <div class="mb-4">
                        <input v-model="editingField.defaultValue" class="input" placeholder="Default Value">
                    </div>
                    <div class="flex justify-end">
                        <button @click="updateClientField" class="btn btn-primary">Update</button>
                        <button @click="closeEditModal" class="btn btn-secondary ml-2">Cancel</button>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts">
import axios from "axios";
import { API_URL } from "@/utils/constants";
import {ClientField, Client as MediaClient} from "@/models";
import {generateGuid} from "@/utils/numbers";
import {createClientField, deleteClientField, fetchClientFieldByClientId, updateClientField} from "@/api/clients";

export default defineComponent({
     props: {
        client: {
            type: Object as () => MediaClient,
            required: true
        } // Define the prop for the client object
     },
    data() {
        return {
            newField: {
                name: "",
                defaultValue: "",
                clientId: this.client.clientId // Pass the client ID to the new field
            } as ClientField,
            clientFields: [] as ClientField[],
            editingField: {} as ClientField,
            showEditModal: false
        };
    },
    async mounted() {
         if(!this.client.clientId) {
             console.error("Client ID is blank");
             return;
         }
        this.clientFields = await fetchClientFieldByClientId(this.client.clientId);
    },
    methods: {

        async createClientField() {
             console.log("Creating client field:", this.newField);
                 await createClientField(this.newField)
                 this.clientFields = await fetchClientFieldByClientId(this.client.clientId);
        },
        async updateClientField() {
            const field = await updateClientField(this.editingField);
            try {
                const index = this.clientFields.findIndex(field => field.clientFieldId === this.editingField.clientFieldId);
                if (index !== -1) {
                    this.clientFields[index] = field;
                }
                this.closeEditModal();
            } catch (error) {
                console.error("Error updating client field:", error);
            }
        },
        async deleteClientField(clientFieldId: string | undefined) {
            await deleteClientField(clientFieldId);
            this.clientFields = this.clientFields.filter(field => field.clientFieldId !== clientFieldId);

        },
        async openEditModal(field: ClientField) {
            this.editingField = { ...field };
            this.showEditModal = true;
        },
        closeEditModal() {
            this.showEditModal = false;
            this.editingField = {defaultValue: "", name: "", clientId: this.client.clientId} as ClientField;
        }
    }
});
</script>

<style scoped>
/* Add your Tailwind CSS classes and custom styles here */
</style>
``
