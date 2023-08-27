<template v-if="event">
    <ContextMenu :event="event" :items="menu" />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import ContextMenu from '@/components/ui/ContextMenu.vue';
import {MenuRow} from "@/models/menu";
import {MenuItem} from "@headlessui/vue";
import {MediaListItem, } from "@/models";
import {useListStore} from "@/store/listStore";

export default defineComponent( {
    name: "MediaListContextMenu",
    components: {
        ContextMenu
    },
    props: {
        event: Object as () => Event | null,
        selectedItem: Object as () => MediaListItem | null,

    },
    setup({event, selectedItem}) {
        const listStore = useListStore();


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
                    if (selectedItem && selectedItem.mediaItemId) {
                        console.log("Deleting item:", selectedItem);
                        // await deleteMediaListItem(selectedItem.value.mediaItemId);
                        await listStore.removeListItem(selectedItem.mediaListId, selectedItem.mediaItemId);
                    }
                }
            },
            {
                label: 'Send to List',
                action: async () => {
                    console.log("Copying item to list:", selectedItem);
                }
            },
            {
                label: 'Edit Poster',
                action: async () => {
                    // default poster with path set to this posters path.
                    console.log("Update Poster list:", selectedItem);
                }
            },
            {
                label: 'Get Provider Poster',
                action: async () => {
                    if (selectedItem && selectedItem.mediaItemId) {
                        await listStore.updateListItemPoster(selectedItem.mediaItemId);

                    }
                }
            },
            {
                label: 'IMDB',
                action: async () => {
                    console.log("Navigating to IMDB:", selectedItem);
                    //TODO: add check for imdb for this label
                    window.open(`https://www.imdb.com/title/${selectedItem?.item?.providers?.imdbId}`, '_blank');
                }
            },
            {
                label: 'Add to Sonarr / Radarr',
                action: async () => {
                    // Todo: Implement this and have it check what type and if its a movie vs tv show and then add it to the correct agent
                    console.log("Adding item to Sonarr / Radarr:", selectedItem);
                    requestModal.value?.openModal(selectedItem);
                }
            },

        ];


        return {
            menu: contextMenuItems,
        };
    }
});
</script>

<style scoped>
/* Add any specific styles if required for the MediaListActionMenu */
</style>
