<template>
  <Modal :is-open="isOpen" :cancel-action="closeModal" :do-action="doAction">
      <h2 class="text-white text-xl font-bold mb-4">Sync List</h2>
      <p class="text-white mb-2">{{ mediaListItem?.name}}</p>
      <p class="text-indigo-300 mb-4">This request will be approved.</p>

      <!-- Flex container for 3 sections -->
      <div class="flex justify-between mb-4 space-x-2">

        <div class="flex-1">
          <label class="block text-white text-sm font-bold mb-2" for="quality">List Type</label>
          <select id="quality" class="block appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500">
            <!-- ... existing options -->
          </select>
        </div>

        <div class="flex-1">
          <label class="block text-white text-sm font-bold mb-2" for="folder">Libraries</label>
          <select id="folder" class="block appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500">
            <!-- ... existing options -->
          </select>
        </div>




        <div class="flex-1">
          <label class="block text-white text-sm font-bold mb-2" for="tags">Tags</label>
          <input type="text" class="appearance-none block w-full bg-gray-700 text-white border border-gray-600 rounded py-2 px-4 mb-3 leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500" id="tags" placeholder="Enter tags">
        </div>

      </div>

      <div class="mb-4">
        <label class="block text-white text-sm font-bold mb-2" for="tags">Sync to</label>
        <ClientButtonGroup :type="ClientType.MEDIA_SERVER" />
      </div>


      <div class="mb-4 space-y-2">
          <label class="block text-white text-sm font-bold">Options:</label>

          <div>
              <input type="checkbox" id="updateImages" v-model="mediaListOptions.updateImages">
              <label for="updateImages" class="text-white ml-2">Update client poster images</label>
          </div>
          <div>
              <input type="checkbox" id="deleteExisting" v-model="mediaListOptions.deleteExisting">
              <label for="deleteExisting" class="text-white ml-2">Delete list if one with same name exists.</label>
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
import { defineComponent, ref } from 'vue';
import {MediaListItem, ClientType, MediaListOptions} from "@/models";
import ClientButtonGroup from "@/components/ui/ClientButtonGroup.vue";
import Modal from "@/components/ui/Modal.vue";

export default defineComponent({
  name: 'MediaListOptionsPopup',
  components: {ClientButtonGroup, Modal},
  setup() {
    const isOpen = ref(false);
    const mediaListItem = ref<MediaListItem>();
      const mediaListOptions = ref<MediaListOptions>({
          mediaListOptionsId: '',
          mediaListId: '',
          syncLibraryId: '',
          sync: false,
          updateImages: false,
          deleteExisting: false,
      });

    const doAction = () => {
      // Implement the sync logic here
      console.log("Request Sent!");
      isOpen.value = false;
    };

    const openModal = (item: MediaListItem) => {
      mediaListItem.value = item;
      isOpen.value = true;
    };

    const closeModal = () => {
      isOpen.value = false;
    };

    return {
      isOpen,
      openModal,
      ClientType,
      mediaListItem,
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
