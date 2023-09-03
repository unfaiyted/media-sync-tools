<template>
    <div class="p-6 bg-gray-100 min-h-screen" v-if="mediaList.items">
        <!-- Table for Media List Details -->
        <!-- View Mode Toggle -->
      <div class="space-y-4">


      </div>
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-lg font-semibold">{{ mediaList.name }}</h1>

            <div class="mb-4">
                <label class="mr-4">View Mode:</label>
                <input type="radio" id="table" value="table" v-model="viewMode">
                <label for="table" class="mr-4">Table</label>
                <input type="radio" id="poster" value="poster" v-model="viewMode">
                <label for="poster">Poster</label>
            </div>
            <MediaListActionMenu :mediaList="mediaList"/>
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
            </tr>
            </thead>
            <tbody>
            <tr v-for="item in mediaList.items" :key="item.mediaItemId"
                class="hover:bg-gray-100"
                @contextmenu.prevent="handleRightClick($event, item)"

            >

                <td class="py-2 px-4">
                    <input type="checkbox">
                </td>
                <td class="py-2 px-4">
                    <img :src="item?.item?.poster" :alt="item?.name" class="max-w-full h-20 mb-2">
                </td>
                <td class="py-2 px-4">{{ item?.item?.title }} ({{ item?.item?.year || item?.item?.releaseDate }})</td>
                <td class="py-2 px-4">
                  {{ item?.item?.type }}
<!--                  <MediaListContainedInListTooltip :containedInLists="listDataForThisItem" />-->
                </td>
                <td class="py-2 px-4">{{ item?.item?.sortTitle }}</td>
                <td class="py-2 px-4">{{ mediaList?.clientId }}</td>


                <!-- Add other data fields as needed -->
            </tr>
            </tbody>
        </table>

        <!-- Poster View -->
        <div v-else-if="viewMode === 'poster'" class="flex flex-wrap">
            <div v-for="item in mediaList.items" :key="item.mediaItemId"
                 class="w-1/6 p-4 flex flex-col items-center poster-container"
                 @contextmenu.prevent="handleRightClick($event, item)">
                <img :src="item.item?.poster" :alt="item.item?.tagline" class="max-w-full h-auto mb-2">
                <span class="text-center">{{ item.item?.title }} ({{ item.item?.year || item.item?.releaseDate }})</span>
            </div>
        </div>



        <MediaItemContextMenu
            :event="contextMenuEvent"
        />


    </div>
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import {MediaListItem, MediaListOptions, MediaList, MediaItem} from "@/models";
import ContextMenu from "@/components/ui/ContextMenu.vue";
import MediaListActionMenu from "@/components/list/MediaListActionMenu.vue";
import MediaListOptionsPopup from "@/components/list/MediaListOptionsPopup.vue";
import {useListStore} from "@/store/listStore";
import MediaItemContextMenu from "@/components/list/MediaItemContextMenu.vue";
import MediaListContainedInListTooltip from "@/components/list/MediaListContainedInListTooltip.vue";

export default defineComponent({
    name: 'MediaItemsList',
    components: {MediaListContainedInListTooltip, MediaItemContextMenu, MediaListOptionsPopup, ContextMenu, MediaListActionMenu},
    props: {
        mediaList: {
            type: Object as () => MediaList,
            required: true,
            default: () => ({items: []})
        },
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


        function handleRightClick(event: Event, item: MediaListItem) {
            const store = useListStore();
            event.preventDefault();
            console.log("Right click", event, item)
            contextMenuEvent.value = event;
            store.setSelectedItem(item);
        }




        return {
            showOptionsPopup,
            requestModal,
            viewMode,
            selectedItem,
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

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */
{
    opacity: 0;
}

.poster-container {
    transition: transform 0.3s ease;
    transform-origin: center;
    cursor: pointer; /* Change cursor style to link hand pointer */
    z-index: 1; /* Ensure scaled image is above others */
}

.poster-container:hover {
    transform: scale(1.1); /* Slightly enlarge the image */
}
</style>
