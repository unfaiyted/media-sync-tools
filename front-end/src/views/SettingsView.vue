<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <h1 class="text-2xl font-semibold mb-4">Settings</h1>

    <!-- Button to trigger the modal -->
    <button @click="showModal = true" class="bg-blue-500 text-white px-4 py-2 rounded shadow mb-4">Add Client</button>

    <!-- List of Added Clients -->
    <div v-for="config in clientsConfig" :key="config.id" class="bg-white p-4 rounded shadow-lg mb-4">
      <h3 class="text-lg font-semibold">{{ config.clientName }} - {{ config.name }}</h3>
      <ul>
        <li v-for="(value, key) in config.fields" :key="key">{{ key }}: {{ value }}</li>
      </ul>
      <button @click="deleteClient(config.id)" class="mt-2 bg-red-500 text-white px-4 py-2 rounded shadow">Delete</button>
    </div>

    <!-- Modal for Adding Clients -->
    <!-- ... (rest of the modal) -->

    <div v-if="showModal" class="fixed top-0 left-0 w-full h-full flex items-center justify-center">
      <div class="bg-white p-4 rounded shadow-lg w-1/2">
        <h2 class="text-lg font-semibold mb-4">Add a Client</h2>

        <label for="client-select" class="block mb-2">Select Client</label>
        <select v-model="selectedClient" id="client-select" class="border p-2 rounded w-full mb-4">
          <option disabled value="">Please select one</option>
          <option v-for="client in clients" :key="client.type" :value="client.type">{{ client.name }}</option>
        </select>



        <div v-if="selectedClient">
          <label :for="uniqueName" class="block mb-2">Unique Name</label>
          <input :id="uniqueName" v-model="uniqueName" type="text" class="border p-2 rounded w-full mb-4">
          <div v-for="field in clientFields[selectedClient]" :key="field.id">
            <!-- In the modal, after selecting the client type, add: -->
            <label :for="field.id" class="block mb-2">{{ field.label }}</label>
            <input :id="field.id" :type="field.type || 'text'" class="border p-2 rounded w-full mb-4">
          </div>
        </div>

        <div class="flex justify-end">
          <button @click="showModal = false" class="text-gray-600 px-4 py-2 rounded shadow mr-2">Cancel</button>
          <button @click="addClient" class="bg-green-500 text-white px-4 py-2 rounded shadow">Add</button>
        </div>
      </div>
    </div>

    <!-- ... (rest of your settings) -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      showModal: false,
      selectedClient: '',
      uniqueName: '',
      clients: [
        { type: 'trakt', name: 'Trakt' },
        { type: 'tmdb', name: 'TMDb' },
        // ... other clients
      ],
      clientFields: {
        trakt: [
          { id: 'trakt-api-key', label: 'API Key', type: 'text' },
          { id: 'trakt-username', label: 'Username', type: 'text' },
          // ... other fields
        ],
        tmdb: [
          { id: 'tmdb-api-key', label: 'API Key', type: 'text' },
          // ... other fields
        ],
        // ... other client configurations
      },
      clientsConfig: []  // To store added clients configurations
    }
  },
  methods: {
    async addClient() {
      const clientName = this.clients.find(client => client.type === this.selectedClient).name;
      const fields = {};

      this.clientFields[this.selectedClient].forEach(field => {
        const fieldValue = document.getElementById(field.id).value;
        fields[field.label] = fieldValue;
      });

      // const name = a

      const newClient = {
        id: Date.now(),  // To generate a unique key for Vue's list rendering
        clientName,
        name: this.uniqueName,
        fields
      };

      // Mocked API call to create client
      // try {
      //   const response = await fetch('http://localhost:3000/clients', {
      //     method: 'POST',
      //     headers: {
      //       'Content-Type': 'application/json',
      //     },
      //     body: JSON.stringify(newClient),
      //   });
      //
      //   if (response.ok) {
          this.clientsConfig.push(newClient);
      //   } else {
      //     console.error('Failed to create client');
      //   }
      // } catch (error) {
      //   console.error('There was an error:', error);
      // }

      this.showModal = false;
    },

    async deleteClient(id) {
      // Mocked API call to delete client
      try {
        const response = await fetch(`http://localhost:3000/clients/${id}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          this.clientsConfig = this.clientsConfig.filter(client => client.id !== id);
        } else {
          console.error('Failed to delete client');
        }
      } catch (error) {
        console.error('There was an error:', error);
      }
    }
  }
}
</script>
