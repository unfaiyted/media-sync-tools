<template>
    <div class="p-4 bg-white shadow-lg rounded-lg max-w-5xl mx-auto">
        <h1 class="text-2xl font-bold mb-4">{{ task.taskName }}</h1>
        <p class="mb-6">{{ task.taskDescription }}</p>

        <!-- Task Schedule -->
        <div class="mb-4">
            <h2 class="text-xl font-medium">Schedule</h2>
            <p>Type: {{ task.schedule.type }}</p>
            <p>Details: {{ task.schedule.details }}</p>
            <p>Time Zone: {{ task.schedule.timeZone }}</p>
        </div>

        <!-- Task Status -->
        <div class="mb-4">
            <h2 class="text-xl font-medium">Status</h2>
            <p>Last Run Time: {{ task.status.lastRunTime }}</p>
            <p>Next Run Time: {{ task.status.nextRunTime }}</p>
            <p>State: {{ task.status.state }}</p>
            <p v-if="task.status.error">Error: {{ task.status.error }}</p>
        </div>

        <!-- Task Metadata -->
        <div class="mb-4">
            <h2 class="text-xl font-medium">Metadata</h2>
            <p>Created By: {{ task.metadata.createdBy }}</p>
            <p>Created On: {{ task.metadata.createdOn }}</p>
            <p>Last Modified: {{ task.metadata.lastModified }}</p>
            <p>Tags: {{ task.metadata.tags.join(', ') }}</p>
            <p>Priority: {{ task.metadata.priority }}</p>
        </div>

        <!-- Task Logs -->
        <div class="mb-4">
            <h2 class="text-xl font-medium">Logs</h2>
            <ul>
                <li v-for="log in task.logs" :key="log.timestamp">
                    {{ log.timestamp }} - {{ log.type }}: {{ log.message }}
                </li>
            </ul>
        </div>

        <!-- Task Payload -->
        <div class="mb-4">
            <h2 class="text-xl font-medium">Payload</h2>
            <p>API Key: {{ task.payload.apiKey }}</p>
            <p>Endpoint URL: {{ task.payload.endpointUrl }}</p>
            <p>File Path: {{ task.payload.filePath }}</p>
            <p>Parameters: {{ task.payload.parameters }}</p>
            <p>Additional Config: {{ task.payload.additionalConfig }}</p>
        </div>

        <!-- Actions (Edit and Delete buttons for now) -->
        <div class="mt-6">
            <button @click="editTask" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 mr-2">Edit</button>
            <button @click="deleteTask" class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:ring-offset-2">Delete</button>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        task: {
            type: Object,
            required: true
        }
    },
    watch: {
        taskDetails: {
            deep: true,
            handler(newVal) {
                this.$emit('update:modelValue', newVal);
            }
        }
    },
    methods: {
        editTask() {
            // Emit event to parent to handle the edit action
            this.$emit('editTask', this.task);
        },
        deleteTask() {
            // Emit event to parent to handle the delete action
            this.$emit('deleteTask', this.task);
        }
    }
}
</script>
