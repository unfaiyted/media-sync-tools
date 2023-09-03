<template v-if="event">
    <ContextMenu :event="event" :items="menu"/>
    <MediaItemOptionsPopup
        v-if="selectedItem"
        :selectedItem="selectedItem"
        ref="optionsPopup"
    />
</template>

<script lang="ts">
import {defineComponent, ref, watch,computed} from 'vue';
import ContextMenu from '@/components/ui/ContextMenu.vue';
import {MenuRow} from "@/models/menu";
import {MenuItem} from "@headlessui/vue";
import {MediaListItem,} from "@/models";
import {useListStore} from "@/store/listStore";
import MediaItemOptionsPopup from "@/components/list/MediaItemOptionsPopup.vue";

export default defineComponent({
    name: "MediaItemContextMenu",
    components: {
        MediaItemOptionsPopup,
        ContextMenu
    },
    props: {
        event: Object as () => Event | null
    },
    setup({event}) {
        const listStore = useListStore();
        const showOptionsPopup = ref(false);
        const optionsPopup = ref<InstanceType<typeof MediaItemOptionsPopup> | null>(null);
        const selectedItem = computed(() => listStore.getLastSelectedItem());


        watch(() => event, (newVal, oldVal) => {
            console.log("Event changed", newVal, oldVal);
        })
        // const addToGrabber = async () => {

        const contextMenuItems = computed(() => [
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
                    if (!optionsPopup.value) {
                        console.log("No options popup found");
                        return;
                    }

                    if (!selectedItem) {
                        console.log("No selected item found");
                        return;
                    }
                    // Todo: Implement this and have it check what type and if its a movie vs tv show and then add it to the correct agent
                    console.log("Adding item to Sonarr / Radarr:", selectedItem);
                    // ue?.openModal(selectedItem);
                    optionsPopup.value.openModal(selectedItem);
                }
            },

        ]);


        return {
            menu: contextMenuItems,
            selectedItem,
            optionsPopup
        };
    }
});
</script>

<style scoped>
/* Add any specific styles if required for the MediaListActionMenu */
</style>
