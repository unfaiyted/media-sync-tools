<template>
    <div class="p-6 bg-gray-100 min-h-screen">
        <!-- Table for Media List Details -->
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-lg font-semibold">{{ mediaList.name }}</h1>

            <!-- Button to trigger popup -->
            <button @click="showOptionsPopup = true" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300">
              +
            </button>

        </div>

        <table class="min-w-full bg-white rounded-lg shadow-md">
            <thead>
            <tr class="text-gray-600 text-left">
                <th class="py-2 px-4">Select</th>
                <th class="py-2 px-4">Name</th>
                <th class="py-2 px-4">Type</th>
                <th class="py-2 px-4">Sort Name</th>
                <th class="py-2 px-4">Client ID</th>
                <!-- Add other headers as needed -->

            </tr>
            </thead>
            <tbody>
            <tr v-for="item in mediaList.items" :key="item.itemId"
                class="hover:bg-gray-100"
                @contextmenu.prevent="handleRightClick($event, item)"

            >
                <td class="py-2 px-4">
                    <input type="checkbox">
                </td>
                <td class="py-2 px-4">{{ item.name }} ({{ item.year || item.releaseDate}})</td>
                <td class="py-2 px-4">{{ item.type }}</td>
                <td class="py-2 px-4">{{ mediaList.sortName }}</td>
                <td class="py-2 px-4">{{ mediaList.clientId }}</td>
                <!-- Add other data fields as needed -->
            </tr>
            </tbody>
        </table>

      <ContextMenu
          :event="contextMenuEvent"
          :items="contextMenuItems"
          ref="contextMenu"
      />
      <MediaListOptionsPopup ref="requestModal" />

        <!-- Popup for Media List Options -->
        <transition name="fade">
            <div v-if="showOptionsPopup" class="fixed top-0 left-0 w-full h-full flex items-center justify-center z-50">
                <div class="bg-white p-6 rounded-lg shadow-md w-1/3">
                    <form @submit.prevent="updateOptions">
                        <label class="block mb-4">
                            <span class="text-gray-700">Sync:</span>
                            <input type="checkbox" v-model="mediaListOptions.sync" class="ml-2">
                        </label>
                        <label class="block mb-4">
                            <span class="text-gray-700">Update Images:</span>
                            <input type="checkbox" v-model="mediaListOptions.updateImages" class="ml-2">
                        </label>
                        <!-- Add other form fields as needed -->
                        <div class="flex justify-end">
                            <button type="submit" class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300 mr-2">
                                Save
                            </button>
                            <button @click="showOptionsPopup = false" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-300">
                                Close
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import {MediaListItem, MediaListOptions} from "@/models";
import ContextMenu from "@/components/ui/ContextMenu.vue";
import {deleteMediaList, deleteMediaListItem} from "@/api/lists";
import {useRouter} from "vue-router";
import MediaListOptionsPopup from "@/components/list/MediaListOptionsPopup.vue";
const router = useRouter();

export default defineComponent({
    name: 'MediaList',
  components: {MediaListOptionsPopup, ContextMenu},
    props: {
        mediaList: {
            type: Object as () => MediaList,
            required: true
        } ,
        mediaListOptions: {
            type: Object as () => MediaListOptions,
            required: true
        }
    },
    setup(props) {
        const showOptionsPopup = ref(false);
      const contextMenuEvent = ref<Event | null>(null); // Store the event that triggers the context menu
      const selectedItem = ref<MediaListItem | null>(null);  // Store the selected list item for context operations
      const requestModal = ref<InstanceType<typeof MediaListOptionsPopup> | null>(null);

      function updateOptions() {
            // Handle logic to update the MediaList options
            console.log("Updated options:", props.mediaListOptions);
            showOptionsPopup.value = false;
        }

        function handleRightClick(event: Event, item: MediaListItem) {
          event.preventDefault();
          contextMenuEvent.value = event;
          selectedItem.value = item; // Store the selected list item for context operations
        }


      const contextMenuItems = [
        {
          label: 'Edit',
          action: async () => {
            // router.push(`/list/${selectedItem.value.mediaListId}/edit`);
          }
        },
        {
          label: 'Delete',
          action: async () => {
            console.log("Deleting item:", selectedItem.value);
            await deleteMediaListItem(selectedItem.value.mediaItemId);
          }
        },
        {
          label: 'Copy to list',
          action: async () => {
            console.log("Copying item to list:", selectedItem.value);
          }
        },
        {
          label: 'Add to Sonarr / Radarr',
          action: async () => {
            // Todo: Implement this and have it check what type and if its a movie vs tv show and then add it to the correct agent
            console.log("Adding item to Sonarr / Radarr:", selectedItem.value);
            requestModal.value?.openModal(selectedItem.value);
          }
        },

      ];

        return {
          showOptionsPopup,
          updateOptions,
          requestModal,
          contextMenuItems,
          contextMenuEvent,
          handleRightClick,
        };
    }
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
    opacity: 0;
}
</style>
