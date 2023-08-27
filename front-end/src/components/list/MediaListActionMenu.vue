<template v-if="event">
    <ContextMenu :event="event" :items="menu" />
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import ContextMenu from '@/components/ui/ContextMenu.vue';
import {MenuRow} from "@/models/menu";
import {MenuItem} from "@headlessui/vue";

export default defineComponent( {
    name: "MediaListActionMenu",
    components: {
        ContextMenu
    },
    props: {
        show: {
            type: Boolean,
            default: false
        },
        event: Object as () => Event | null,
        menu: {
            type: Object as () => MenuRow[],
            default: () => [
                {
                    label: "Play",
                    action: () => console.log("Play clicked!")
                },
                [
                    {
                        label: "Add to Queue",
                        action: () => console.log("Add to Queue clicked!")
                    },
                    {
                        label: "Download",
                        action: () => console.log("Download clicked!")
                    }
                ],
                {
                    type: 'divider'
                },
                {
                    label: "Delete",
                    action: () => console.log("Delete clicked!")
                }
            ],
        },
    },
    setup(props) {
        // Define the menu specific for the MediaListActionMenu
        console.log('props', props)
        return {
            event: props.event,
            menu: props.menu
        };
    }
});
</script>

<style scoped>
/* Add any specific styles if required for the MediaListActionMenu */
</style>
