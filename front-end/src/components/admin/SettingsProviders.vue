<template>
  <div class="p-4">

    <!-- Display Buttons for Adding Provider -->
    <div class="mb-4 flex space-x-2">
      <button @click="addProvider" class="bg-blue-500 text-white px-4 py-2 rounded">Add Provider</button>
    </div>

    <!-- Display Providers grouped by ClientType -->
    <div v-for="clientType in clientTypes" :key="clientType">
      <h2 class="text-xl mb-4">{{ formatHeader(clientType) }}</h2>

      <!-- Display Providers in Modern Cards -->
      <div class="grid grid-cols-3 gap-4 mb-4">
        <div v-for="provider in getProvidersByType(clientType)" :key="provider.client.clientId"
             @click="handleCardClick(provider)"
             class="cursor-pointer bg-white border p-4 rounded-lg shadow-md">


          <div class="relative group">
            <button
                @click.stop="openDeleteModal(provider)"
                class="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full w-8 h-8 flex justify-center items-center group-hover:opacity-100 opacity-0 transition-opacity duration-300"
            >
              X
            </button>
          </div>

          <!-- Logo Image -->
          <div :class="getPlaceholderClass(provider.client.name)">
            <span class="text-white text-4xl font-semibold">{{ getInitial(provider.client.name) }}</span>
          </div>

          <!-- Provider Name -->
          <div class="text-center mb-2">{{ provider.client.name }}</div>

          <!-- Client Type Settings -->
          <div v-if="clientType === 'MEDIA_SERVER'" class="text-center space-y-2">
            <button @click="syncLibraries" class="bg-yellow-500 text-white px-4 py-2 rounded">Sync Libraries</button>
            <div class="flex items-center justify-center mt-2">
              <input type="checkbox" v-model="autoSync" class="mr-2">
              <label>Auto-sync libraries</label>
            </div>
          </div>

          <!-- Add more provider specific details here -->



          <Modal :isOpen="showProviderDetailsModal"
                 @do-action="saveProviderChanges"
                  do-action-text="Save Changes"
                  cancel-action-text="Cancel"
                 @cancel-action="showProviderDetailsModal = false">
            <div class="p-4">

              <h3 class="text-xl mb-4">Edit Provider: {{ selectedProvider?.client.name }}</h3>
              <div>
                <!-- Sample input field for editing provider name -->
                <label class="block mb-2">Provider Name:</label>
                <input v-model="selectedProvider.client.name" class="border p-2 rounded w-full mb-4">

                <!-- Add more input fields for other properties here -->


              </div>
            </div>
          </Modal>

        </div>
      </div>
    </div>

  </div>

  <Modal :isOpen="showProviderManagerModal"
         @do-action="addProvider"
         do-action-text="Add Provider"
         @cancel-action="showProviderManagerModal = false">
    <ProviderManager :config="config" ref="providerManager"/>
  </Modal>


  <Modal :isOpen="showDeleteModal" @cancel-action="closeDeleteModal">
    <div class="p-4">
      Are you sure you want to delete {{ selectedProvider?.client.name }}?
      <div class="mt-4 flex justify-end space-x-4">
        <button @click="closeDeleteModal" class="bg-gray-300 hover:bg-gray-400 px-4 py-2 rounded">
          Cancel
        </button>
        <button @click="deleteProvider" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
          Delete
        </button>
      </div>
    </div>
  </Modal>


</template>


<script lang="ts">
import {ref, onMounted} from 'vue';
import {ClientType, Library} from "@/models";
import Modal from "@/components/ui/Modal.vue";
import LibraryManager from "@/components/config/LibraryManager.vue";
import ProviderManager from "@/components/config/ProviderManager.vue";
import {useAppConfigStore} from "@/store/appConfigStore";

export default {
  name: 'SettingsProviders',
  components: {Modal, LibraryManager, ProviderManager},


  setup() {

    const store = useAppConfigStore();
    const autoSync = ref(false);
    const selectedProvider = ref(null);
    const showDeleteModal = ref(false);
    const showProviderManagerModal = ref(false);

    onMounted(async () => {
      // Assuming you need to hydrate the store when component mounts. Adjust as needed.
      await store.hydrateApp('APP-DEFAULT-USER');
    });

    const clientTypes = computed(() => {
      // Extract the unique client types from the clients
      const types = store.appConfig?.clients?.map(client => client.client.type) || [];
      return [...new Set(types)];
    });

    const getProvidersByType = (type: ClientType) => {
      return store.appConfig?.clients?.filter(client => client.client.type === type) || [];
    };

    const syncLibraries = () => {
      // Logic to sync libraries. Might need to call an API or dispatch an action here.
      console.log('Syncing libraries...');
    };

    const appConfigStore = useAppConfigStore();

    const getInitial = (name: string) => {
      return name.charAt(0).toUpperCase();
    };


    const openDeleteModal = (provider) => {
      selectedProvider.value = provider;
      showDeleteModal.value = true;
    };

    const closeDeleteModal = () => {
      selectedProvider.value = null;
      showDeleteModal.value = false;
    };

    const formatHeader = (str: string) => {
      return str
          .toLowerCase()
          .split('_')
          .map(word => word.charAt(0).toUpperCase() + word.slice(1))
          .join(' ');
    };


    const colors = ['bg-purple-300', 'bg-blue-300', 'bg-red-300', 'bg-yellow-300', 'bg-green-300'];

    const getPlaceholderClass = (name: string) => {
      const charCode = name.charCodeAt(0);
      const colorIndex = charCode % colors.length;
      return `h-24 w-24 mx-auto mb-4 rounded-full ${colors[colorIndex]} flex items-center justify-center`;
    };

    const deleteProvider = async () => {
      if (selectedProvider.value) {
        // TODO: Add your delete logic here using the selected provider
        // Example: await api.deleteProvider(selectedProvider.value.id);

        // After deleting, close the modal and refresh the list (or remove the provider from the local list)
        closeDeleteModal();
      }
    };
    const showProviderDetailsModal = ref(false);

    const handleCardClick = (provider) => {
      console.log('Clicked provider', provider);
      selectedProvider.value = provider;
      showProviderDetailsModal.value = true;
    };

    const closeProviderDetailsModal = () => {
      showProviderDetailsModal.value = false;
    };

    const saveProviderChanges = async () => {
      if (selectedProvider.value) {
        // TODO: Add your save/update logic here using the selected provider
        // Example: await api.updateProvider(selectedProvider.value);

        // After updating, close the modal and refresh the list (or update the provider in the local list)
        closeProviderDetailsModal();
      }
    };

    const addProvider = () => {
      showProviderManagerModal.value = true;
    };

    return {
      autoSync,
      addProvider,
      getInitial,
      clientTypes,
      openDeleteModal,
      handleCardClick,
  closeProviderDetailsModal,
      showDeleteModal,
      showProviderManagerModal,
      showProviderDetailsModal,
  saveProviderChanges,
      closeDeleteModal,
      getProvidersByType,
      selectedProvider,
      deleteProvider,
      syncLibraries,
      appConfigStore,
      formatHeader,
      getPlaceholderClass,
    };
  }
};
</script>
