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
                label: 'Clone list',
                action: async () => {
                    // router.push(`/list/${selectedItem.value.mediaListId}/edit`);
                    // update sourceListId as mediaListId
                    // update mediaListId as new mediaListId
                }
            },
            {
                label: 'Edit list',
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
                label: 'Edit Poster',
                action: async () => {
                    // default poster with path set to this posters path.
                    console.log("Update Poster list:", selectedItem);
                }
            },
            {
                label: 'Go to Provider',
                action: async () => {
                    console.log("Navigating to Provider list", selectedItem);
                    //TODO: add check for imdb for this label
                    window.open(`https://www.imdb.com/title/${selectedItem?.item?.providers?.imdbId}`, '_blank');
                }
            },
            {
                label: 'Add to Sonarr / Radarr',
                action: async () => {
                    // Todo: Implement this and have it check what type and if its a movie vs tv show and then add it to the correct agent
                    console.log("Adding item to Sonarr / Radarr:", selectedItem);
                    // ue?.openModal(selectedItem);
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
