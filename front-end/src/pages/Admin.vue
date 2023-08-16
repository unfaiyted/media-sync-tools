<template>
    <div>
        <!-- Create Client -->
        <h2>Create Client</h2>
        <input v-model="client.clientId" placeholder="Client ID">
        <input v-model="client.label" placeholder="Label">
        <select v-model="client.type">
            <!-- Assuming ClientType is an enum with values 'TypeA', 'TypeB', etc. -->
            <option value="TypeA">TypeA</option>
            <option value="TypeB">TypeB</option>
            <!-- Add other types as needed -->
        </select>
        <input v-model="client.name" placeholder="Client Name">
        <!-- For simplicity, I'm skipping LibraryClients and ConfigClient lists here.
             You'd typically have other components or UI mechanisms to manage these. -->

        <button @click="createClient">Add Client</button>

        <!-- List Clients -->
        <h2>Clients</h2>
        <ul v-if="clients.length">
            <li v-for="client in clients" :key="client.clientId">
                {{ client.name }} ({{ client.clientId }}, {{ client.label }}, {{ client.type }})
                <button @click="deleteClient(client.clientId)">Delete</button>
            </li>
        </ul>

        <!-- Update Client (can be improved with a modal or separate component) -->
        <h2>Update Client</h2>
        <input v-model="updatedClient.clientId" placeholder="Client ID">
        <input v-model="updatedClient.label" placeholder="Label">
        <select v-model="updatedClient.type">
            <option value="TypeA">TypeA</option>
            <option value="TypeB">TypeB</option>
            <!-- Add other types as needed -->
        </select>
        <input v-model="updatedClient.name" placeholder="Client Name">
        <!-- Similarly, skipping LibraryClients and ConfigClient here -->

        <button @click="updateClient">Update Client</button>
    </div>
</template>

<script>
import axios from "axios";
import {API_URL} from "@/utils/constants";

export default {
    data() {
        return {
            clients: [],
            client: {
                clientId: '',
                label: '',
                type: '',  // You'd set a default type here if needed
                name: '',
                LibraryClients: [],
                ConfigClient: []
            },
            updatedClient: {
                clientId: '',
                label: '',
                type: '',
                name: '',
                LibraryClients: [],
                ConfigClient: []
            }
        };
    },
    async mounted() {
        this.clients = await this.fetchClients();
    },
    methods: {
        async fetchClients() {
            try {
                const response = await axios.get(`${API_URL}/clients`);
                return response.data;
            } catch (error) {
                console.error("Error fetching clients:", error);
            }
        },
        async createClient() {
            try {
                await axios.post(`${API_URL}/clients`, this.client);
                this.clients = await this.fetchClients();
            } catch (error) {
                console.error("Error creating client:", error);
            }
        },
        async deleteClient(clientId) {
            try {
                await axios.delete(`${API_URL}/clients/${clientId}`);
                this.clients = await this.fetchClients();
            } catch (error) {
                console.error("Error deleting client:", error);
            }
        },
        async updateClient() {
            try {
                await axios.put(`${API_URL}/clients/${this.updatedClient.clientId}`, this.updatedClient);
                this.clients = await this.fetchClients();
            } catch (error) {
                console.error("Error updating client:", error);
            }
        }
    }
};
</script>
