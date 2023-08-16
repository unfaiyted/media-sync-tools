<template>
    <div class="p-6">
        <!-- Create Client -->
        <h2 class="text-lg font-semibold mb-4">Create Client</h2>
        <div class="mb-4">
            <input v-model="client.label" class="input" placeholder="Label">
        </div>
        <div class="mb-4">
            <select v-model="client.type" class="input">
                <option value="MEDIA_SERVER">Media Server</option>
                <option value="LIST_PROVIDER">List Provider</option>
                 <option value="UTILITY">Utility</option>
                <!-- Add other types as needed -->
            </select>
        </div>
        <div class="mb-4">
            <input v-model="client.name" class="input" placeholder="Client Name">
        </div>
        <button @click="create" class="btn btn-primary">Add Client</button>

        <!-- List Clients -->
        <h2 class="text-lg font-semibold mt-8 mb-4">Clients</h2>
        <ul v-if="clients.length">
            <li v-for="client in clients" :key="client.clientId" class="mb-2">
                {{ client.name }} ({{ client.clientId }}, {{ client.label }}, {{ client.type }})
                <button @click="openEditModal(client)" class="btn btn-secondary">Edit</button>
                <button @click="deleteItem(client.clientId)" class="btn btn-danger">Delete</button>
            </li>
        </ul>

        <!-- Update Client Modal -->
        <transition name="modal" enter-active-class="transition-opacity ease-out duration-300" leave-active-class="transition-opacity ease-in duration-300">
            <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center">
                <div class="modal-overlay absolute inset-0 bg-gray-900 opacity-75" @click="closeEditModal"></div>
                <div class="modal-container fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white w-1/2 p-6 rounded shadow-lg">
                    <h3 class="text-lg font-semibold mb-4">Edit Client</h3>
                      <input v-model="updatedClient.clientId" class="input" placeholder="Client ID" disabled>
                    <div class="mb-4">
                        <input v-model="updatedClient.label" class="input" placeholder="Label">
                    </div>
                    <div class="mb-4">
                        <select v-model="updatedClient.type" class="input">
                            <option value="MEDIA_SERVER">Media Server</option>
                            <option value="LIST_PROVIDER">List Provider</option>
                            <option value="UTILITY">Utility</option>
                        </select>
                    </div>
                    <div class="mb-4">
                        <input v-model="updatedClient.name" class="input" placeholder="Client Name">
                    </div>

                    <ClientFieldManagement :client="updatedClient"/>
                    <div class="flex justify-end">
                        <button @click="update" class="btn btn-primary">Update</button>
                        <button @click="closeEditModal" class="btn btn-secondary ml-2">Cancel</button>
                    </div>
                </div>
            </div>
        </transition>


        <ClientsConfig config="config"/>

        <!-- ... (rest of the template) -->
    </div>
</template>

<script lang="ts">
import axios from "axios";
import {API_URL} from "@/utils/constants";
import ClientFieldManagement from "@/components/admin/ClientFieldManagement.vue";
import {generateGuid} from "@/utils/numbers";
import {Client, ClientType} from "@/models";
import {createClient, deleteClient, fetchClients, updateClient} from "@/api/clients";

import ClientsConfig from "@/components/config/ClientsConfig.vue";
export default defineComponent({
    components: {
        ClientFieldManagement,
        ClientsConfig
    },
    data() {
        return {
            clients: [] as Client[],
            client: {
                clientId: "TEST_CLIENT_ID",
                label: '',
                type: ClientType.UNKNOWN,  // You'd set a default type here if needed
                name: '',
                LibraryClients: [],
                ConfigClient: []
            } as Client,
            updatedClient: {
                clientId: '',
                label: '',
                type: ClientType.UNKNOWN,
                name: '',
                LibraryClients: [],
                ConfigClient: []
            } as Client,
            showEditModal: false,
            editingClient: null
        };
    },
    async mounted() {
        this.clients = await fetchClients();
        console.log("Clients", this.clients);
    },
    methods: {
        openEditModal(client: any) {
            this.editingClient = client;
            this.updatedClient = { ...client };
            this.showEditModal = true;
        },

        // Close the edit modal
        closeEditModal() {
            this.showEditModal = false;
            this.editingClient = null;
            this.updatedClient = {
                clientId: "",
                label: "",
                type: ClientType.UNKNOWN,
                name: "",
                LibraryClients: [],
                ConfigClient: []
            } as Client
        },
        async create() {
            await createClient(this.client);
            this.clients = await fetchClients();
        },
        async deleteItem(clientId: string | undefined) {
            if(!clientId) {
                console.error("Client ID blank", clientId);
                return;
            }
            await deleteClient(clientId);
           this.clients = await fetchClients();
        },
        async update() {
            await updateClient(this.updatedClient);
            this.clients = await fetchClients();
            this.closeEditModal();
        }
    }
});
</script>


<style scoped>
/* Add your custom styles here if needed */
</style>
