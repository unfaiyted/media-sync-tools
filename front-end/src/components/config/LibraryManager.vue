<template>
    <div class="p-6 bg-grey-800">
        <h1 class="text-xl font-bold mb-4 text-white">Add Library Management</h1>
        <div class="mb-4 flex">
            <input v-model="newLibraryName" class="block appearance-none w-[100%] bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500" placeholder="Library Name" />
<!--            <button @click="createLibrary" class="px-4 py-2 bg-blue-500 text-white rounded ml-2">Create Library</button>-->
        </div>
         <div class="mb-4 flex">
           <div class="flex flex-col">
             <!-- Dropdown for LibraryType -->
             <label class="block font-semibold text-white mb-2 mr-3 w-[50%]">Type</label>

             <select v-model="selectedLibraryType" class="block mr-3appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500">
               <option disabled value="">Please select one</option>
               <option v-for="(value, name) in LibraryType" :key="name" :value="value">
                 {{ toReadableString(name) }}
               </option>
             </select>
           </div>
           <div class="w-1/2  pl-4">
                <h2 class="text-md font-semibold mb-2 text-white">Selected Clients</h2>
                <select v-model="selectedConfigClients" multiple class="block appearance-none w-full  bg-gray-700 border border-gray-600 text-white py-2 px-2 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500">
                    <option v-for="configClient in possibleConfigClients" :key="configClient.clientId" :value="configClient">
                        {{ configClient.label }}
                    </option>
                </select>
            </div>
<!--            <button @click="createLibrary" class="px-4 py-2 bg-blue-500 text-white rounded ml-2">Create Library</button>-->
        </div>
        <div class="flex flex-col">

                <h2 class="text-md font-semibold mb-2 text-white" >Library Names</h2>
            <div class="w-full flex ">
                <div v-for="configClient in selectedConfigClients" :key="configClient.clientId" class=" p-2 mb-2 w-full rounded">
                    <h3 class="text-lg font-semibold text-white">{{ configClient.label }}</h3>
                    <input v-model="clientLibraryNames[configClient.clientId]" class="block appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500" :placeholder="'Library Name for ' + configClient.label" />
                </div>
            </div>

        </div>


<!--      <div class="flex">
        <div class="mt-4 mr-1">
&lt;!&ndash;            <button @click="addLibraryClients" class="px-4 py-2 bg-green-500 text-white rounded">Add Clients</button>&ndash;&gt;
        </div>
        <div class="mt-4">
&lt;!&ndash;            <button @click="submitLibraryClients" class="px-4 py-2 bg-blue-500 text-white rounded">Submit</button>&ndash;&gt;
        </div>-->
<!--      </div>-->


        <!-- List Config Clients -->
        <h2 class="text-md font-semibold mt-8 mb-4 text-white">Library Client Mapping</h2>
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
</template>

<script lang="ts">
import {onMounted, ref} from 'vue';
import {
  createLibrary,
  createLibraryClient,
  deleteLibrary,
  deleteLibraryClient,
  fetchLibraries,
  fetchLibraryClients
} from '@/api/libraries';
import {fetchConfigClientsByConfigId} from "@/api/configs";
import {Config, ConfigClient, Library, LibraryClient, LibraryType} from "@/models";
import {generateGuid} from "@/utils/numbers";
import {toReadableString} from "../../utils/string";


export default defineComponent({
  computed: {
    LibraryType() {
      return LibraryType
    }
  },
    methods: {toReadableString, deleteLibrary, deleteLibraryClient},
    props: {
        config: {
            required: true,
            type: Object as () => Config
        }
    },
    async mounted() {
        const libraries = await fetchLibraries();
        this.libraries = libraries;
        for (const library of libraries) {
            if(library.libraryId === undefined) continue;
            const clients = await fetchLibraryClients(library.libraryId)
            this.libraryClients = [...this.libraryClients, ...clients]
            console.log(this.libraryClients)
        }
    },
    setup(props: { config: Config }) {
        const newLibraryName = ref('');
        const selectedLibraryType = ref<LibraryType>(LibraryType.UNKNOWN);
        const possibleConfigClients = ref<Array<ConfigClient>>([]);
        const selectedConfigClients = ref<Array<ConfigClient>>([]);
        const libraries = ref<Array<Library>>([]);
        const libraryClients = ref<Array<LibraryClient>>([]);
        const lastLibrary = ref<Library>();
        const clientLibraryNames = ref<{ [key: string]: string }>({});
        const configId = props.config.configId; // Extract configId from the props

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
          selectedLibraryType,
            libraryClients,
            createLibrary: createLib,
            getConfigClient,
            filteredLibraryClients,
            addLibraryClients,
            deleteLib
        };
    }
});
</script>

<style scoped>
/* Add your custom styles here */
</style>
