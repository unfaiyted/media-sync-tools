<template>
    <VButton @click="showActionsMenu($event)" label="Actions" />
    <ContextMenu :event="actionMenuEvent" :items="actionMenu" />
</template>

<script lang="ts">
import {defineComponent, ref} from 'vue';
import ContextMenu from '@/components/ui/ContextMenu.vue';
import {useTaskStore} from "@/store/taskStore";
import {MediaList, ScheduleType, Task, TaskPriority, TaskState} from "@/models";
import VButton from "@/components/ui/inputs/Button.vue";


export default defineComponent( {
    name: "MediaListActionMenu",
    components: {
        VButton,
        ContextMenu
    },
    props: {
        mediaList: Object as () => MediaList,
        event: Object as () => Event | null,
    },
    setup({ mediaList }) {
        // Define the menu specific for the MediaListActionMenu
        const showActionMenu = ref(false);  // To determine which context menu to display
        const actionMenuEvent = ref<Event | null>(null); // Store the event that triggers the context menu
        const actionMenu = [
            {
                label: "Sync",
                action: async () => {

                    // const configClientId
                    // Need to derive the configClientId and figure out a ui for getting that

                    console.log("Sync clicked!");
                    const taskStore = useTaskStore();

                    const task: Task = {
                        logs: [],
                        payload: {
                            listId: mediaList?.mediaListId,
                            configClientId: mediaList?.configClientId,
                            action: "sync"
                        },
                        metadata: {
                            createdOn: new Date(),
                            createdBy: "admin",
                            lastModified: new Date(),
                            tags: ['sync','list'],
                            priority: TaskPriority.MEDIUM
                        },
                        schedule: {
                            type: ScheduleType.INTERVAL,
                            details: {
                                interval: 60
                            },
                            timeZone: "America/Chicago",
                        },
                        status: {
                            lastRunTime: new Date(),
                            nextRunTime: new Date(),
                            state: TaskState.CREATED
                        },
                        taskDescription: `Syncing Media list ${mediaList?.name}`,
                        taskName: `Sync Media List ${mediaList?.name}`,
                        taskId: crypto.randomUUID()

                    }

                    const resultTask = await taskStore.createTask(task);
                    await taskStore.triggerTaskOnDemand(resultTask.taskId)

                }
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
                label: "Delete List",
                action: () => console.log("Delete clicked!")
            }
        ]
        function showActionsMenu(event: Event) {
            actionMenuEvent.value = event;
            // showActionMenu.value = true;  // Display the MediaListActionMenu
            console.log('showActionsMenu', showActionMenu.value);
        }

        return {
            showActionsMenu,
            actionMenu,
            showActionMenu,
            actionMenuEvent,
        };
    }
});
</script>

<style scoped>
/* Add any specific styles if required for the MediaListActionMenu */
</style>
