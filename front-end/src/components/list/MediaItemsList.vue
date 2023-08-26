<template>
    <div class="p-6 bg-gray-100 min-h-screen" v-if="mediaList.items">
        <!-- Table for Media List Details -->
        <!-- View Mode Toggle -->

        <div class="flex justify-between items-center mb-4">
            <h1 class="text-lg font-semibold">{{ mediaList.name }}</h1>

          <div class="mb-4">
            <label class="mr-4">View Mode:</label>
            <input type="radio" id="table" value="table" v-model="viewMode">
            <label for="table" class="mr-4">Table</label>
            <input type="radio" id="poster" value="poster" v-model="viewMode">
            <label for="poster">Poster</label>
          </div>
            <!-- Button to trigger popup -->
            <button @click="showOptionsPopup = true" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300">
             Actions
            </button>
        </div>

      <table v-if="viewMode === 'table'" class="min-w-full bg-white rounded-lg shadow-md">
            <thead>
            <tr class="text-gray-600 text-left">
                <th class="py-2 px-4">Select</th>
                <th class="py-2 px-4">Poster</th>
                <th class="py-2 px-4">Name</th>
                <th class="py-2 px-4">Type</th>
                <th class="py-2 px-4">Sort Name</th>
                <th class="py-2 px-4">Client ID</th>
                <!-- Add other headers as needed -->

            </tr>
            </thead>
            <tbody>
<!--            {{ mediaList.items}}-->
            <tr v-for="item in mediaList.items" :key="item.mediaItemId"
                class="hover:bg-gray-100"
                @contextmenu.prevent="handleRightClick($event, item)"

            >

                    <td class="py-2 px-4">
                        <!--&lt;!&ndash;                     {{ item}}&ndash;&gt; {{item}}-->
                        <input type="checkbox">
                    </td>
                    <td class="py-2 px-4">
                        <img :src="item?.item?.poster" :alt="item?.name" class="max-w-full h-20 mb-2">
                    </td>
                    <td class="py-2 px-4">{{ item?.item?.title }} ({{ item?.item?.year || item?.item?.releaseDate}})</td>
                    <td class="py-2 px-4">{{ item?.item?.type }}</td>
                    <td class="py-2 px-4">{{ item?.item?.sortTitle}}</td>
                    <td class="py-2 px-4">{{ mediaList?.clientId }}</td>


                <!-- Add other data fields as needed -->
            </tr>
            </tbody>
        </table>


      <!-- Poster View -->
      <div v-else-if="viewMode === 'poster'" class="flex flex-wrap">
        <div v-for="item in mediaList.items" :key="item.mediaItemId"
             class="w-1/6 p-4 flex flex-col items-center"
             @contextmenu.prevent="handleRightClick($event, item)"

        >
          <img :src="item.item?.poster" :alt="item.item?.tagline" class="max-w-full h-auto mb-2">
          <span class="text-center">{{ item.item.title }} ({{ item.item.year || item.item.releaseDate }})</span>
        </div>
      </div>

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

        <Modal
<!--            :event="contextMenuEvent"
            :items="contextMenuItems"
            ref="contextMenu"-->
        >
        <MediaListOptionsPopup ref="requestModal" />
        </Modal>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import {MediaListItem, MediaListOptions, MediaList, MediaItem} from "@/models";
import ContextMenu from "@/components/ui/ContextMenu.vue";
import MediaListOptionsPopup from "@/components/list/MediaListOptionsPopup.vue";
import {useListStore} from "@/store/listStore";

export default defineComponent({
    name: 'MediaItemsList',
  components: {MediaListOptionsPopup, ContextMenu},
    props: {
        mediaList: {
            type: Object as () => MediaList,
            required: true,
            default: () => ({ items: []})
        } ,
        mediaListOptions: {
            type: Object as () => MediaListOptions,
            required: true
        },
        item: {
            type: Object as () => MediaItem
            ,
            required: false,
            default: () => ({})
        }
    },
    setup(props) {
        const showOptionsPopup = ref(false);
      const contextMenuEvent = ref<Event | null>(null); // Store the event that triggers the context menu
      const selectedItem = ref<MediaListItem | null>(null);  // Store the selected list item for context operations
      const requestModal = ref<InstanceType<typeof MediaListOptionsPopup> | null>(null);
      const viewMode = ref('table'); // Default view mode
      const listStore = useListStore();
      const mediaList = ref(props.mediaList);

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
            if(selectedItem.value && selectedItem.value.mediaItemId) {
              console.log("Deleting item:", selectedItem.value);
              // await deleteMediaListItem(selectedItem.value.mediaItemId);
              mediaList.value = await listStore.removeListItem(selectedItem.value.mediaListId, selectedItem.value.mediaItemId);
            }
          }
        },
        {
          label: 'Send to List',
          action: async () => {
            console.log("Copying item to list:", selectedItem.value);
          }
        },
        {
           label: 'Edit Poster',
          action: async () => {
               // default poster with path set to this posters path.
            console.log("Update Poster list:", selectedItem.value);
          }
        },
        {
          label: 'Get Provider Poster',
          action: async () => {
            if(selectedItem.value && selectedItem.value.mediaItemId) {
              mediaList.value = await listStore.updateListItemPoster(selectedItem.value.mediaItemId);

            }
          }
        },
        {
          label: 'IMDB',
          action: async () => {
            console.log("Navigating to IMDB:", selectedItem.value);
            //TODO: add check for imdb for this label
            window.open(`https://www.imdb.com/title/${selectedItem?.value?.item?.providers?.imdbId}`, '_blank');
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
          viewMode,
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
