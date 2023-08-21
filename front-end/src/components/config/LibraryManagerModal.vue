<template>
  <Modal :is-open="isOpen">
    <div class="p-6">
      <h1 class="text-3xl font-bold mb-4">Library Client Mapping Management</h1>
      <div class="mb-4">
        <input v-model="newLibraryName" class="px-4 py-2 rounded border" placeholder="Library Name" />
        <button @click="createLibrary" class="px-4 py-2 bg-blue-500 text-white rounded ml-2">Create Library</button>
      </div>
      <div class="flex">
        <div class="w-1/2 pr-4">
          <h2 class="text-xl font-semibold mb-2">Selected Clients</h2>
          <select v-model="selectedConfigClients" multiple class="px-4 py-2 rounded border w-full">
            <option v-for="configClient in possibleConfigClients" :key="configClient.clientId" :value="configClient">
              {{ configClient.label }}
            </option>
          </select>
        </div>
        <div class="w-1/2 pl-4">
          <h2 class="text-xl font-semibold mb-2">Library Names</h2>
          <div v-for="configClient in selectedConfigClients" :key="configClient.clientId" class="border p-2 mb-2 rounded">
            <h3 class="text-lg font-semibold">{{ configClient.label }}</h3>
            <input v-model="clientLibraryNames[configClient.clientId]" class="px-4 py-2 rounded border w-full" :placeholder="'Library Name for ' + configClient.label" />
          </div>
        </div>
      </div>
      <div class="mt-4">
        <button @click="addLibraryClients" class="px-4 py-2 bg-green-500 text-white rounded">Add Clients</button>
      </div>
      <div class="mt-4">
        <button @click="submitLibraryClients" class="px-4 py-2 bg-blue-500 text-white rounded">Submit</button>
      </div>


      <!-- List Config Clients -->
      <h2 class="text-lg font-semibold mt-8 mb-4">Library Client Mapping</h2>
      <ul v-if="libraries.length">
        <li v-for="library in libraries" :key="library.libraryId" class="mb-4">
          <h3 class="text-md font-semibold">{{ library.name }}</h3>
          <ul v-if="filteredLibraryClients(library.libraryId).length">
            <li v-for="libraryClient in filteredLibraryClients(library.libraryId)" :key="libraryClient.libraryClientId" class="ml-4 mb-2">
              Client: {{ getConfigClient(libraryClient.clientId).label }}, Library: {{ libraryClient.libraryName }}
            </li>
          </ul>
          <button @click="deleteLib(library.libraryId)" class="btn btn-danger">Delete</button>
        </li>
      </ul>

    </div>
  </Modal>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import Modal from '@/components/ui/Modal.vue';
import { fetchConfigClientsByConfigId } from '@/api/configs';
import { Config, ConfigClient, Library, LibraryClient } from '@/models';
import { generateGuid } from '@/utils/numbers';
import {
  fetchLibraries,
  createLibrary,
  deleteLibrary,
  createLibraryClient,
} from '@/api/libraries';

export default defineComponent({
  name: 'LibraryManagerModal',
  components: { Modal },
  props: {
    config: {
      required: true,
      type: Object as () => Config,
    },
  },
  setup(props: { config: Config }) {
        const newLibraryName = ref('');
        const possibleConfigClients = ref<Array<ConfigClient>>([]);
        const selectedConfigClients = ref<Array<ConfigClient>>([]);
        const libraries = ref<Array<Library>>([]);
        const libraryClients = ref<Array<LibraryClient>>([]);
        const lastLibrary = ref<Library>();
        const clientLibraryNames = ref<{ [key: string]: string }>({});
        const configId = props.config.configId; // Extract configId from the props

        const isOpen = ref(false);

        const fetchPossibleConfigClients = async () => {
            try {
                possibleConfigClients.value = await fetchConfigClientsByConfigId(configId);
            } catch (error) {
                console.error('Error fetching possible config clients:', error);
            }
        };


        const filteredLibraryClients = (libraryId: string) => {
            return libraryClients.value.filter(libraryClient => libraryClient.libraryId === libraryId);
        };

        const getConfigClient = (clientId: string) => {
            return possibleConfigClients.value.filter(client => client.clientId === clientId)[0];
        };
        const createLib = async () => {
            try {
                const newLibrary = await createLibrary({
                    libraryId: generateGuid(),
                    name: newLibraryName.value
                });
                libraries.value.push(newLibrary);

                lastLibrary.value = newLibrary;

                // Clear the input field
                newLibraryName.value = '';

                // Add libraryClients
                await addLibraryClients();

            } catch (error) {
                console.error('Error creating library:', error);
            }
        };

        const deleteLib = async (libraryId: string | undefined) => {
            try {
                await deleteLibrary(libraryId);
                libraries.value = libraries.value.filter(library => library.libraryId !== libraryId);
            } catch (error) {
                console.error('Error deleting library:', error);
            }
        };

        const addLibraryClients = async () => {
            if (selectedConfigClients.value.length === 0) {
                console.warn('No clients selected');
                return;
            }

            try {
                // Prepare data for adding library clients
                const libraryClientsToAdd = selectedConfigClients.value.map(configClient => {
                    return {
                        libraryClientId: generateGuid(), // Assign libraryId appropriately
                        libraryId: lastLibrary.value.libraryId ,
                        libraryName: clientLibraryNames.value[configClient.clientId],
                        clientId: configClient.clientId
                    };
                });

                libraryClients.value = [...libraryClients.value, ...libraryClientsToAdd];

                // Perform API call to add library clients
                await Promise.all(libraryClientsToAdd.map(async libraryClient => {
                    const addedLibraryClient = await createLibraryClient((libraryClient as LibraryClient));
                    // Update the clientLibraryNames object
                    console.log(addedLibraryClient)
                    clientLibraryNames.value[libraryClient.clientId] = addedLibraryClient.libraryName;
                }));

                // Update the libraries' array to reflect the change
                // Fetch updated libraries after adding clients
                console.log(await fetchLibraries());
            } catch (error) {
                console.error('Error adding library clients:', error);
            }
        };

        const submitLibraryClients = async () => {
            // Implement submitting library clients
        };
        // Fetch data on mounted
        onMounted(() => {
            fetchPossibleConfigClients();
        });

        return {
            newLibraryName,
            possibleConfigClients,
            selectedConfigClients,
            libraries,
            submitLibraryClients,
            clientLibraryNames,
            libraryClients,
            createLibrary: createLib,
            getConfigClient,
            filteredLibraryClients,
            isOpen,
            addLibraryClients,
            deleteLib
        };
  },
});
</script>

<style scoped>
/* Add your custom styles here using Tailwind classes */
</style>
