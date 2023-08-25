<template>
    <div class="p-4">
        <div class="mb-4 flex justify-between items-center">
            <h1 class="text-2xl font-semibold">Task Manager</h1>
            <button @click="openNewTaskModal" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">+ New Task</button>
        </div>

        <!-- Task List -->
        <TaskList :tasks="tasks" @viewTask="openViewTaskModal" @editTask="openEditTaskModal"/>

        <!-- Modal for Task Creation and Editing -->
        <Modal :isOpen="isModalOpen" @do-action="handleSave" @cancel-action="closeModal">
            <!-- Task Details -->
            <TaskDetails v-if="selectedTask" v-model="selectedTask"/>
            <ActionBar :task="selectedTask" @triggerTask="handleTriggerTask" @saveTask="handleSave" @deleteTask="handleDelete"/>
        </Modal>


        <button @click="showNewTaskModal = true" class="bg-indigo-500 text-white px-4 py-2 rounded hover:bg-indigo-600">
            New Task
        </button>

        <NewTaskModal
            :isOpen="showNewTaskModal"
            @close-modal="showNewTaskModal = false"
            @task-created="refreshTaskList"
        />

    </div>
</template>

<script>
import TaskList from '@/components/tasks/TaskLists.vue';
import TaskDetails from '@/components/tasks/TaskDetails.vue';
import ActionBar from '@/components/tasks/ActionBar.vue';
import Modal from '@/components/ui/Modal.vue';
import {createTask, fetchAllTasks, updateTask} from "@/api/tasks";
import NewTaskModal from '@/components/tasks/NewTaskModal.vue';

export default {

    components: {
        TaskList,
        NewTaskModal,
        TaskDetails,
        ActionBar,
        Modal
    },
    data() {
        return {
            tasks: [],  // you can populate this from an API call
            isModalOpen: false,
            showNewTaskModal: false,
            selectedTask: null
        };
    },
    methods: {
        openNewTaskModal() {
            this.selectedTask = {};  // Initialize with empty data for new task
            this.isModalOpen = true;
        },
        openViewTaskModal(task) {
            this.selectedTask = Object.assign({}, task);  // Clone the task to avoid direct mutation
            this.isModalOpen = true;
        },
        openEditTaskModal(task) {
            this.selectedTask = Object.assign({}, task);  // Clone the task for editing
            this.isModalOpen = true;
        },
        closeModal() {
            this.isModalOpen = false;
            this.selectedTask = null;  // Clear out the selected task
        },
        async handleSave() {
            if (this.selectedTask.id) {
                // Update existing task
                await updateTask(this.selectedTask.id, this.selectedTask);
            } else {
                // Create a new task
                await createTask(this.selectedTask);
            }
            // Refetch the tasks after creation or update
            this.tasks = await fetchAllTasks();
            this.closeModal();
        },
        handleTriggerTask() {
            // Logic to trigger the task
        },
        handleDelete() {
            // Logic to delete the task
        },
        async refreshTaskList() {
            // Refresh your tasks list here after a new task is created
        }
    }
};
</script>
