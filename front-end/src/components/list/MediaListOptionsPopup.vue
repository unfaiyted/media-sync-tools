<template>
  <Modal :is-open="isOpen" @cancel-action="closeModal" @do-action="doAction">
      <h2 class="text-white text-xl font-bold mb-4">Sync List</h2>
      <p class="text-white mb-2">{{ mediaListItem?.name}}</p>
      <p class="text-indigo-300 mb-4">This request will be approved.</p>

      <!-- Flex container for 3 sections -->
      <div class="flex justify-between mb-4 space-x-2">

        <div class="flex-1">
          <label class="block text-white text-sm font-bold mb-2" for="quality">Copy as Type</label>
          <VSelect :options="mediaListTypes" v-model="mediaListOptions.type" />
        </div>

        <div class="flex-1">
          <label class="block text-white text-sm font-bold mb-2" for="folder">Library to Sync</label>
            <VSelect :options="configLibraries" v-model="mediaListOptions.syncLibraryId" />
        </div>

<!--        <div class="flex-1">
          <label class="block text-white text-sm font-bold mb-2" for="tags">Tags</label>
          <input type="text" class="appearance-none block w-full bg-gray-700 text-white border border-gray-600 rounded py-2 px-4 mb-3 leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500" id="tags" placeholder="Enter tags">
        </div>-->

      </div>

      <div class="mb-4">
        <label class="block text-white text-sm font-bold mb-2" for="tags">Sync to media server(s):</label>
        <ClientButtonGroup :type="ClientType.MEDIA_SERVER" :is-config="true" @selectedClientsChanged="handleSelectedClients" />
      </div>


      <div class="mb-4 space-y-2">
          <label class="block text-white text-sm font-bold">Options:</label>
          <div>
              <VCheckbox v-model="mediaListOptions.updateImages" label="Update client poster images"/>
          </div>
          <div>
              <VCheckbox v-model="mediaListOptions.deleteExisting" label="Delete list if one with same name exists." />
          </div>

      </div>

      <div class="flex items-center mb-4">
        <img src="https://plex.tv/users/8366c34ded926e94/avatar?c=1685649373" alt="User Avatar" class="h-8 w-8 rounded-full mr-4">
        <div>
          <p class="text-white">Faiyt</p>
          <p class="text-sm text-gray-400">unfaiyted@gmail.com</p>
        </div>
      </div>


  </Modal>
</template>

<script lang="ts">
import {defineComponent, onBeforeMount, ref} from 'vue';
import {MediaListItem, ClientType, MediaListOptions, MediaListType, ConfigClient} from "@/models";
import ClientButtonGroup from "@/components/ui/ClientButtonGroup.vue";
import Modal from "@/components/ui/Modal.vue";
import VSelect from "@/components/ui/inputs/Select.vue";
import {SelectOption} from "@/models/ui";
import {useAppConfigStore} from "@/store/appConfigStore";
import VCheckbox from "@/components/ui/inputs/Checkbox.vue";
import {useListStore} from "@/store/listStore";

export default defineComponent({
  name: 'MediaListOptionsPopup',
  components: {VCheckbox, VSelect, ClientButtonGroup, Modal},
  setup(props, {emit}) {
      // const store = useAppConfigStore();
    const configLibraries = ref<SelectOption[]>([]);
    const isOpen = ref(false);
    const mediaListItem = ref<MediaListItem>();
    const selectedClients =  ref<ConfigClient[]>([]);
    const mediaListTypes: SelectOption[] = Object.values(MediaListType).map((type) => {
        return {
            value: type,
            text: type,
        };
    }).filter((type) => type.value !== MediaListType.LIBRARY)
      const mediaListOptions = ref<MediaListOptions>({
          mediaListOptionsId: crypto.randomUUID(),
          userId: '',
          mediaListId: '',
          syncLibraryId: '',
          clients: [],
          type: MediaListType.COLLECTION,
          sync: true,
          updateImages: false,
          deleteExisting: false,
      });

      onBeforeMount(async () => {
          const store = useAppConfigStore();
          configLibraries.value = (await store.getLibraries()).map((library) => {
              return {
                  value: library.libraryId as string,
                  text: library.name,
              };
          })

        });


    const doAction = () => {
      // Implement the sync logic here
        console.log(mediaListOptions.value)
        const listStore = useListStore();
        listStore.syncListToProviders(mediaListOptions.value);
      console.log("Request Sent!");
      isOpen.value = false;
    };

    const openModal = async (item: MediaListItem) => {
        const store = useAppConfigStore();
        mediaListOptions.value.mediaListId = item.mediaListId;
        mediaListOptions.value.userId = (await store.getConfigUser()).userId as string;
      mediaListItem.value = item;
      isOpen.value = true;
    };

    const closeModal = () => {
      isOpen.value = false;
     emit('close-modal');
    };


    const handleSelectedClients = (selectedClients: ConfigClient[]) => {
        console.log('selected clients changed', selectedClients)
        mediaListOptions.value.clients = selectedClients;
      }

    return {
      isOpen,
      openModal,
      ClientType,
      mediaListItem,
        handleSelectedClients,
        selectedClients,
        configLibraries,
        mediaListTypes,
        mediaListOptions,
      doAction,
      closeModal
    };
  }
});
</script>

<style scoped>
/* Optional additional styling */
</style>
