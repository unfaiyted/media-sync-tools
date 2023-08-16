<template>
    <div class="p-6">
        <!-- Create Config Client -->
           <h2 class="text-lg font-semibold mb-4">Create Client Instance</h2>
        <div class="mb-4">
            <input v-model="newConfigClient.label" class="input" placeholder="Label">
        </div>
        <div class="mb-4">
            <select v-model="newConfigClient.clientId" class="input">
                <option v-for="client in possibleClients" :key="client.clientId" :value="client.clientId">
                    {{ client.name }} <!-- Assuming each client object has a name property -->
                </option>
            </select>
        </div>


        <!-- Add other input fields here for other properties of ConfigClient -->
        <button @click="createConfigClient" class="btn btn-primary">Add Config Client</button>

        <!-- List Config Clients -->
        <!-- For this demo, I'm assuming you will fetch a list of Config Clients and store it in a variable named configClients -->
        <h2 class="text-lg font-semibold mt-8 mb-4">Config Clients</h2>
        <ul v-if="configClients.length">
            <li v-for="config in configClients" :key="config.configClientId" class="mb-2">
                {{ config.label }}
                <button @click="openEditModal(config)" class="btn btn-secondary">Edit</button>
                <button @click="deleteConfigClient(config.configClientId)" class="btn btn-danger">Delete</button>
            </li>
        </ul>

        <!-- Update Config Client Modal -->
        <!-- It's essentially similar to the one you provided for ClientField with some names changed -->
        <transition name="modal" enter-active-class="transition-opacity ease-out duration-300" leave-active-class="transition-opacity ease-in duration-300">
            <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center">
                <div class="modal-overlay absolute inset-0 bg-gray-900 opacity-75" @click="closeEditModal"></div>
                <div class="modal-container bg-white w-1/2 mx-auto p-6 rounded shadow-lg">
                    <h3 class="text-lg font-semibold mb-4">Edit Config Client</h3>
                    <div class="mb-4">
                        <input v-model="editingConfigClient.label" class="input" placeholder="Label">
                    </div>
                    <!-- Add other input fields here for editing -->

                    <!-- Dynamic input generation for clientFields -->
                    <div v-for="field in clientFields" :key="field.name" class="mb-4">
                        <label :for="field.name" class="block mb-2">{{ field.name }}</label>
                        <input v-model="editingFields[field.name]"
                               @input="handleInputChange(field)"
                               :id="field.name"
                               class="input"
                               :placeholder="field.defaultValue || 'Enter value'">
                    </div>


                    <div class="flex justify-end">
                        <button @click="updateConfigClient" class="btn btn-primary">Update</button>
                        <button @click="closeEditModal" class="btn btn-secondary ml-2">Cancel</button>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import {Client as MediaClient, ClientField, Config, ConfigClient, ConfigClientFieldsValue} from "@/models";
import { createConfigClient, deleteConfigClient, fetchConfigClientByConfigId, updateConfigClient } from "@/api/configs";
import {fetchClientFieldByClientId, fetchClients} from "@/api/clients";

export default defineComponent({
    props: {
        config: {
            type: Object as () => Config,
            required: true
        } // Define the prop for the client object
    },
    data() {
        return {
            newConfigClient: {
                label: ""
                // initialize other properties here
            } as ConfigClient,
            configClients: [] as ConfigClient[],
            editingConfigClient: {} as ConfigClient,
            showEditModal: false,
            clientFields: [] as ClientField[],
            possibleClients: [] as MediaClient[],
            editingFields: {
                name: ""
            }
        };
    },
    async mounted() {
        // Fetching all configClients for this demo. Adjust as necessary.

        this.possibleClients = await fetchClients(); // Fetch the list of clients when the component mounts
        this.configClients = await fetchConfigClientByConfigId(this.config.configId);

        console.log(this.possibleClients);
    },
    methods: {
         async handleInputChange(field: ClientField) {
            const dataToUpdate: ConfigClientFieldsValue = {
                configClientFieldsId: field.clientFieldId , // you should have some logic or data property to know the ID
                clientField: field,
                configClientId: (this.config.configId) ? this.config.configId : '', // fill this in based on your component data
                value: this.editingFields[field.name]
            };

            try {
                await updateConfigClientFieldsValue(dataToUpdate);
                // maybe show a success message or some other logic after saving
            } catch (error) {
                console.error("Error updating value:", error);
                // maybe show an error message to the user
            }
        },
        async createConfigClient() {
            console.log("Creating config client:", this.newConfigClient);

            if(!this.config || !this.config.configId) {
                console.error("No config provided");
                return;
            }

            this.newConfigClient = {
                ...this.newConfigClient,
                configId: this.config.configId
            }
            await createConfigClient(this.newConfigClient);
            this.configClients = await fetchConfigClientByConfigId(this.config.configId);
        },
        async updateConfigClient() {
            const config = await updateConfigClient(this.editingConfigClient);
            const index = this.configClients.findIndex(cfg => cfg.configClientId === this.editingConfigClient.configClientId);
            if (index !== -1) {
                this.configClients[index] = config;
            }
            this.closeEditModal();
        },
        async deleteConfigClient(configClientId: string | undefined) {
            await deleteConfigClient(configClientId);
            this.configClients = this.configClients.filter(cfg => cfg.configClientId !== configClientId);
        },
        async openEditModal(config: ConfigClient) {
            this.editingConfigClient = { ...config };
            this.clientFields = await fetchClientFieldByClientId(config.clientId);
            this.showEditModal = true;
        },
        closeEditModal() {
            this.showEditModal = false;
            this.editingConfigClient = {} as ConfigClient;
        }
    }
});
</script>

<style scoped>
/* Add your Tailwind CSS classes and custom styles here */
.modal-container {
    z-index: 1000;
}
</style>
