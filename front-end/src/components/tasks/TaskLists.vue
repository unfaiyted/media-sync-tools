<template>
    <div class="container mx-auto p-4">
        <!-- Display tasks in a card layout -->
        <div v-for="task in tasks" :key="task.taskName" class="p-4 m-2 bg-white shadow-md rounded">

            <!-- Task Name and Description -->
            <h2 class="text-xl font-bold">{{ task.taskName }}</h2>
            <p class="text-gray-600">{{ task.taskDescription }}</p>

            <!-- Task Actions -->
            <div class="mt-4">
                <button @click="triggerTask(task.taskName)" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Trigger</button>
                <button @click="editTask(task)" class="px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600 ml-2">Edit</button>
                <button @click="deleteTask(task.taskName)" class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 ml-2">Delete</button>
            </div>

        </div>

        <!-- No tasks message -->
        <div v-if="tasks.length === 0" class="p-4 m-2 bg-white shadow-md rounded text-center">
            No tasks available. Add a new one!
        </div>

    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useTaskStore } from '@/store/taskStore';

const taskStore = useTaskStore();
const tasks = taskStore.tasks;

// Fetch tasks when component mounts
onMounted(() => {
    taskStore.fetchAllTasks();
});

const triggerTask = (taskId) => {
    taskStore.triggerTaskOnDemand(taskId);
};

const editTask = (task) => {
    // Use Vue Router to navigate to the edit task component.
    // Pass the task details for editing.
    // For this, you'll need to have Vue Router set up with an "edit task" route.
};

const deleteTask = (taskId) => {
    taskStore.deleteTask(taskId);
};
</script>

<style>
/* Add any specific styles you want here */
</style>
