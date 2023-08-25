<template>
    <Modal
        :isOpen="isOpen"
        @do-action="saveTask"
        @cancel-action="closeModal"
        doActionText="Save"
        cancelActionText="Cancel"
    >
        <form @submit.prevent="saveTask">
            <!-- Task Name -->
            <label for="taskName" class="block text-sm font-medium text-gray-700">Task Name</label>
            <input v-model="newTask.taskName" id="taskName" type="text" placeholder="Enter task name" required class="mt-1 p-2 w-full border rounded-md">

            <!-- Task Description -->
            <label for="taskDescription" class="block text-sm font-medium text-gray-700 mt-2">Description</label>
            <textarea v-model="newTask.taskDescription" id="taskDescription" placeholder="Enter task description" class="mt-1 p-2 w-full border rounded-md"></textarea>

            <!-- Task Schedule -->
            <label for="scheduleType" class="block text-sm font-medium text-gray-700 mt-2">Schedule Type</label>
            <select v-model="newTask.schedule.type" id="scheduleType" class="mt-1 p-2 w-full border rounded-md">
                <!-- Example values for ScheduleType. Add your actual values. -->
                <option value="type1">Interval</option>
                <option value="type2">Cron</option>
            </select>

            <!-- More fields for other Task properties can be added similarly -->

            <button type="submit" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-4">
                Create Task
            </button>
        </form>
    </Modal>
</template>


<script lang="ts">
import { ref } from 'vue';
import Modal from '@/components/ui/Modal.vue';

import { createTask } from "@/api/tasks";

export default {
    components: {
        Modal
    },
    props: {
        isOpen: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            newTask: {
                taskName: '',
                taskDescription: '',
                schedule: {
                    type: '', // Initialize with default schedule type if necessary
                    details: {}, // Initialize with default details if needed
                    timeZone: '' // Assuming a default timezone can be provided if required
                },
                status: '', // Initialize with default task status if necessary
                metadata: {
                    createdBy: '', // This should likely be set during save based on authenticated user info
                    createdOn: new Date(), // Sets to current date by default
                    lastModified: new Date(), // Sets to current date by default
                    tags: [],
                    priority: '' // Initialize with default priority if necessary
                },
                logs: [],
                payload: {} // Optional, so initialize to empty object. Can also be left undefined.
            }
        };
    },
    methods: {
        async saveTask() {
            try {
                if (this.newTask.taskName) { // Ensure basic validation, adapt as required
                    await createTask(this.newTask);
                    this.$emit('task-created');
                    this.closeModal();
                } else {
                    console.error("Task name is required.");
                    // Show an error or toast to the user indicating required fields
                }
            } catch (error) {
                console.error("Failed to create new task:", error);
                // Optionally display an error message to the user
            }
        },
        closeModal() {
            this.$emit('close-modal');
        }
    }
};
</script>

<style scoped>
/* Any additional styles you'd like for this modal */
</style>
