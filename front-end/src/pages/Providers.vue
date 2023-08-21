<template>
  <div class="p-4">
    <!-- Display Buttons for Adding Provider and Library -->
    <div class="mb-4 flex space-x-2">
      <button @click="addLibrary" class="bg-green-500 text-white px-4 py-2 rounded">Add Library</button>
      <button @click="addProvider" class="bg-blue-500 text-white px-4 py-2 rounded">Add Provider</button>
    </div>

    <!-- Display Library Categories -->
    <div>
      <h2 class="text-xl mb-4">Library:</h2>
      <div v-for="library in libraries" :key="library.libraryId">
        <h3 class="text-lg mb-2">{{ library.name }} ({{ library.type }}):</h3>
        <ul class="list-disc pl-5">
          <li v-for="client in library.clients" :key="client.libraryClientId">
            <a :href="`/provider/${client.clientId}`">{{ client.client?.name }}</a>
            <ul class="list-circle pl-5">
              <li><a :href="`/library/${client.libraryName}`">{{ client.libraryName }}</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>


  <Modal :isOpen="showLibraryManagerModal" @close="showLibraryManagerModal = false" :cancel-action="closeLibraryModal">
    <LibraryManager :config="config" />
  </Modal>

  <Modal :isOpen="showProviderManagerModal" @close="showProviderManagerModal = false" :cancel-action="closeProviderModal">
    <ProviderManager :config="config" />
  </Modal>

</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import {LibraryType} from "@/models";
import {fetchConfig} from "@/api/configs";
import Modal from "@/components/ui/Modal.vue";
import LibraryManager from "@/components/config/LibraryManager.vue";
import ProviderManager from "@/components/config/ProviderManager.vue";


export default {
  name: 'Providers',
  components: {Modal, LibraryManager, ProviderManager},
  data() {
    return {
      config: {
        configId: 'APP-DEFAULT-CONFIG'
      },
      libraries: [{
        libraryId: 1,
        name: 'Movies',
        type: LibraryType.MOVIES,
        clients: [{
          libraryClientId: 1,
          libraryName: 'Movies',
          clientId: 1,
          client: {
            clientId: 1,
            name: 'Plex',
          },
        }, {
          libraryClientId: 2,
          libraryName: 'Movies',
          clientId: 2,
          client: {
            clientId: 2,
            name: 'Emby',
          },
        }],
      }], // This should be fetched from the backend
    };
  },
  setup() {
    const showLibraryManagerModal = ref(false);
    const showProviderManagerModal = ref(false);

    return {
      showLibraryManagerModal,
      showProviderManagerModal
    };
  },
  methods: {
    addProvider() {
      // Logic to add a new provider
      this.showProviderManagerModal = true;
    },
    addLibrary() {
      // Logic to add a new library
      this.showLibraryManagerModal = true;
    },
    async fetchLibraries() {
      // Fetch libraries and their clients from the backend.
      // For demonstration purposes, using a placeholder URL.
      const response = await fetch('/api/libraries');
      this.libraries = await response.json();
    },
    closeProviderModal() {
      this.showProviderManagerModal = false;
    },
    closeLibraryModal() {
      this.showLibraryManagerModal = false;
    }

  },
  async mounted() {
    // Fetch the libraries when the component is mounted
    this.libraries =  this.fetchLibraries();
    this.config = await fetchConfig(this.configId);
  },
};
</script>

<style scoped>
/* Add your Tailwind styles here */
</style>
