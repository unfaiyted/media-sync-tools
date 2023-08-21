<template>
    <div>
        <!-- Loading indicator -->

        <!-- Content to show when not loading -->
            <!-- Dropdown filter for ClientType -->
            <!-- Uncomment the select if needed -->
            <!-- <select v-model="selectedClientType" @change="fetchClients">
              <option v-for="type in clientTypes" :key="type" :value="type">{{ type }}</option>
            </select> -->

            <!-- Display the clients as buttons -->
            <div v-if="!loading" :class="buttonContainerClass">
              <button
                  v-for="client in clients"
                  :key="client.clientId"
                  :class="getButtonClass(client.clientId)"
                  @click="toggleButton(client.clientId)"
              >
                {{ client.label }}
              </button>
            </div>
<!--            <div v-else>
                No clients found.
            </div>-->
        </div>
</template>


<script lang="ts">
import { defineComponent, ref, onBeforeMount } from 'vue';
import {  fetchClientsByType,  } from '@/api/clients';
import {fetchConfigClientsByConfigId, fetchConfigClientsByType} from '@/api/configs'
import {ClientType, ConfigClient} from "@/models"; // Adjust the path accordingly

export default defineComponent({
  name: 'ClientButtonGroup',
  props: {
    type: {
      type: String as () => ClientType,
      default: ClientType.UNKNOWN
    },
    blockStyle: {
      type: Boolean,
      default: true
    },
      isConfig: {
        type: Boolean,
          default: true
      },
    maxWidth: {
      type: String,
      default: 'max-w-md'
    }
  },
  setup(props, context) {
    const clients = ref<(Client|ConfigClient)[]>([]);
    const selectedClientType = ref<ClientType>(ClientType.UNKNOWN);
    const clientTypes = Object.values(ClientType);
    const loading = ref(true);
    const toggledClients = ref<Record<string, boolean>>({}); // Store which clients are toggled



    const getButtonClass = (clientId: string) => {
      return {
        'm-2': !props.blockStyle,
        'w-full border-t border-t-0 w-[125px]': props.blockStyle,
        'bg-blue-500 text-white rounded px-4 py-2 ': toggledClients.value[clientId],
        'bg-gray-400 text-white rounded px-4 py-2': !toggledClients.value[clientId]
      };
    };

    // If the list of clients changes, ensure each has an entry in toggledClients (default to false)
    watchEffect(() => {
      clients.value.forEach(client => {
        if (toggledClients.value[client.clientId] === undefined) {
          toggledClients.value[client.clientId] = false;
        }
      });
    });


    const buttonClass = computed(() => ({
      'm-2': !props.blockStyle,
      'w-full border-t first:border-t-0 border-0': props.blockStyle,
      'bg-blue-500 text-white rounded px-4 py-2': true
    }));

    const buttonContainerClass = computed(() => ({
      'flex flex-wrap': true,
      [props.maxWidth]: true
    }));

    const fetchClients = async () => {
        try {
            if (props.isConfig) {
                clients.value = await fetchConfigClientsByType(config.configId, props.type);
            } else {
                clients.value = await fetchClientsByType(props.type);
            }
            console.log('got clients', clients.value, props.type);
        } catch (error) {
            console.error("Error fetching clients:", error);
        }
        loading.value = false;
        console.log('Not Loading')
    };

      const getLabel = (client: Client | ConfigClient) => {
          return (client as ConfigClient).label || (client as Client).label;
      };

      const toggleButton = (client: Client | ConfigClient) => {
          const clientId = (client as ConfigClient).clientId || client.clientId;
          toggledClients.value[clientId] = !toggledClients.value[clientId];
          context.emit('update:toggledClients', toggledClients.value);
      };

    onBeforeMount(fetchClients)


    return {
      clients,
        getLabel,
        toggleButton,
      selectedClientType,
      loading,
      clientTypes,
      buttonClass,
      getButtonClass,
      buttonContainerClass,
      fetchClients
    };
  }
});
</script>
