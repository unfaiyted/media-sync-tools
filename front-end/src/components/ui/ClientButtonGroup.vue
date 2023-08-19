<template>
    <div>
        <!-- Loading indicator -->
        <div v-if="loading">
            Loading clients...
        </div>

        <!-- Content to show when not loading -->
        <div v-else>
            <!-- Dropdown filter for ClientType -->
            <!-- Uncomment the select if needed -->
            <!-- <select v-model="selectedClientType" @change="fetchClients">
              <option v-for="type in clientTypes" :key="type" :value="type">{{ type }}</option>
            </select> -->

            <!-- Display the clients as buttons -->
            <div v-if="clients.length">
                <button v-for="client in clients" :key="client.clientId" class="m-2 bg-blue-500 text-white rounded px-4 py-2">
                    {{ client.label }}
                </button>
            </div>
            <div v-else>
                No clients found.
            </div>
        </div>
    </div>
</template>


<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import {  fetchClientsByType } from '@/api/clients';
import {ClientType} from "@/models"; // Adjust the path accordingly

export default defineComponent({
  name: 'ClientButtonGroup',
  props: {
    type: {
      type: String,
      default: ClientType.UNKNOWN
    }
  },
  setup(props) {
    const clients = ref<Client[]>([]);
    const selectedClientType = ref<ClientType>(ClientType.UNKNOWN);
    const clientTypes = Object.values(ClientType);

    const fetchClients = async () => {
      try {
        clients.value = await fetchClientsByType(selectedClientType.value);
        console.log(clients.value)
      } catch (error) {
        console.error("Error fetching clients:", error);
      }
    };


    fetchClients()

    watch(() => props.type, async (newType) => {
      clients.value = await fetchClientsByType(newType as ClientType);
    }, { immediate: true });
    // Fetch clients initially when component mounts
    onMounted(fetchClients);

    return {
      clients,
      selectedClientType,
      clientTypes,
      fetchClients
    };
  }
});
</script>
