<template>
  <div class="p-4">
    <!-- Display Buttons for Adding Provider and Library -->
    <div class="mb-4 flex space-x-2">
      <button @click="addLibrary" class="bg-green-500 text-white px-4 py-2 rounded">Add Library</button>
      <button @click="addProvider" class="bg-blue-500 text-white px-4 py-2 rounded">Add Provider</button>
    </div>

    <!-- Display Library Categories -->
    <div>
      <h2 class="text-xl mb-4">Server Libraries:</h2>
      <div v-for="library in libraries" :key="library.libraryId">
        <h3 class="text-lg mb-2">{{ library.name }} ({{ library.type }}):</h3>
        <ul class="list-disc pl-5">
          <li v-for="client in library.clients" :key="client.libraryClientId">
            <a :href="`/provider/${client.clientId}`">{{ client.client?.name }}</a>
            <ul class="list-circle pl-5">
              <li><a :href="`/library/${client.libraryName}`">{{ client.libraryName }}
              </a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>


  <Modal :isOpen="showLibraryManagerModal"
         @do-action="addLibrary"
         @cancel-action="showLibraryManagerModal = false">
    <LibraryManager :config="config" ref="libraryManager"/>
  </Modal>

  <Modal :isOpen="showProviderManagerModal"
         @do-action="addProvider"
         do-action-text="Add Provider"
         @cancel-action="showProviderManagerModal = false">
    <ProviderManager :config="config" ref="providerManager" />
  </Modal>



</template>
<script lang="ts">
import { ref, onMounted } from 'vue';
import {Library} from "@/models";
import Modal from "@/components/ui/Modal.vue";
import LibraryManager from "@/components/config/LibraryManager.vue";
import ProviderManager from "@/components/config/ProviderManager.vue";
import {useAppConfigStore} from "@/store/appConfigStore";

export default {
  name: 'SettingsProviders',
  components: {Modal, LibraryManager, ProviderManager},

  setup() {
    const config = ref({
      configId: 'APP-DEFAULT-CONFIG'
    });
    const libraries = ref<Library[]>([]);
    const showLibraryManagerModal = ref<boolean>(false);
    const showProviderManagerModal = ref<boolean>(false);

    const libraryManager = ref<InstanceType<typeof LibraryManager> | null>(null);
    const providerManager = ref<InstanceType<typeof ProviderManager> | null>(null);

    onMounted(async () => {
      const store = useAppConfigStore();
      libraries.value = (await store.getLibraries()) || [];
      config.value = await store.getAppConfig('APP-DEFAULT-USER');
    });

    const addProvider = () => {
      showProviderManagerModal.value = true;
      providerManager.value?.createConfigClient();
    };

    const addLibrary = () => {
      showLibraryManagerModal.value = true;
      libraryManager.value?.createLib();
    };

    const closeProviderModal = () => {
      showProviderManagerModal.value = false;
    };

    const closeLibraryModal = () => {
      showLibraryManagerModal.value = false;
    };

    return {
      config,
      libraries,
      showLibraryManagerModal,
      showProviderManagerModal,
      libraryManager,
      providerManager,
      addProvider,
      addLibrary,
      closeProviderModal,
      closeLibraryModal
    };
  }
};
</script>
