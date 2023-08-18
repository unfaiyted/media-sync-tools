<template>
  <transition name="fade" enter-active-class="transition-opacity duration-300" leave-active-class="transition-opacity duration-300" enter-class="opacity-0" enter-to-class="opacity-100" leave-class="opacity-100" leave-to-class="opacity-0">
    <div v-if="isOpen" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-800 p-5 rounded-lg shadow-lg w-3/4 max-w-xl z-50">
      <h2 class="text-white text-xl font-bold mb-4">Request Movie</h2>
      <p class="text-white mb-2">{{ mediaListItem?.name}}</p>
      <p class="text-indigo-300 mb-4">This request will be approved.</p>

      <div class="mb-4">
        <label class="block text-white text-sm font-bold mb-2" for="quality">Quality Profile</label>
        <select id="quality" class="block appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500">
          <!-- These are just examples, adjust as needed -->
          <option>Any</option>
          <option>SD</option>
          <option>HD-720p</option>
          <option>HD-1080p</option>
          <option>Ultra-HD</option>
          <option selected>HD - 720p/1080p (Default)</option>
        </select>
      </div>

      <div class="mb-4">
        <label class="block text-white text-sm font-bold mb-2" for="folder">Root Folder</label>
        <select id="folder" class="block appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500">
          <option>/movies</option>
          <option>/e/movies</option>
          <option selected>/f/movies (0 Bytes) (Default)</option>
        </select>
      </div>

      <div class="mb-4">
        <label class="block text-white text-sm font-bold mb-2" for="tags">Servers</label>
        <!-- Adjust this section for the tags, this is just a placeholder for now -->
        <input type="text" class="appearance-none block w-full bg-gray-700 text-white border border-gray-600 rounded py-2 px-4 mb-3 leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500" id="tags" placeholder="Enter tags">
      </div>

      <!-- You might want to refine this if you use a real avatar and email -->
      <div class="flex items-center mb-4">
        <img src="https://plex.tv/users/8366c34ded926e94/avatar?c=1685649373" alt="User Avatar" class="h-8 w-8 rounded-full mr-4">
        <div>
          <p class="text-white">Faiyt</p>
          <p class="text-sm text-gray-400">unfaiyted@gmail.com</p>
        </div>
      </div>

      <div class="flex justify-end">
        <button @click="sendSync" class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 mr-2">Request</button>
        <button @click="closeModal" class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">Cancel</button>
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import {MediaListItem} from "@/models";

export default defineComponent({
  name: 'MediaListOptionsPopup',

  setup() {
    const isOpen = ref(false);
    const mediaListItem = ref<MediaListItem>();

    const sendSync = () => {
      // Implement the sync logic here
      console.log("Request Sent!");

      // Close the modal after sending
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
      mediaListItem,
      sendSync,
      closeModal
    };
  }
});
</script>

<style scoped>
/* Optional additional styling */
</style>
