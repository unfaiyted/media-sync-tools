<template>
    <div class="p-4 bg-white shadow-lg rounded-lg max-w-4xl mx-auto">
        <h1 class="text-2xl font-bold mb-4">{{ isEditing ? 'Edit Task' : 'Create Task' }}</h1>

        <!-- Task Name and Description -->
        <div class="mb-4">
            <label for="taskName" class="block text-sm font-medium text-gray-700">Task Name</label>
            <input v-model="task.taskName" type="text" id="taskName" class="mt-1 p-2 w-full rounded-md shadow-sm border border-gray-300 focus:ring-indigo-500 focus:border-indigo-500">
        </div>

        <div class="mb-4">
            <label for="taskDescription" class="block text-sm font-medium text-gray-700">Task Description</label>
            <textarea v-model="task.taskDescription" id="taskDescription" rows="3" class="mt-1 p-2 w-full rounded-md shadow-sm border border-gray-300 focus:ring-indigo-500 focus:border-indigo-500"></textarea>
        </div>

        <!-- Schedule -->
        <div class="mb-4">
            <label for="scheduleType" class="block text-sm font-medium text-gray-700">Schedule Type</label>
            <select v-model="task.schedule.type" id="scheduleType" class="mt-1 p-2 w-full rounded-md shadow-sm border border-gray-300 focus:ring-indigo-500 focus:border-indigo-500">
                <option value="interval">Interval</option>
                <option value="cron">Cron</option>
                <option value="date">Date</option>
            </select>
        </div>

        <!--... Add details and timeZone fields similarly for TaskSchedule ...-->

        <!-- Task Status -->
        <div class="mb-4">
            <label for="taskState" class="block text-sm font-medium text-gray-700">Task State</label>
            <select v-model="task.status.state" id="taskState" class="mt-1 p-2 w-full rounded-md shadow-sm border border-gray-300 focus:ring-indigo-500 focus:border-indigo-500">
                <option value="running">Running</option>
                <option value="paused">Paused</option>
                <option value="failed">Failed</option>
                <!--... Other state options ...-->
            </select>
        </div>

        <!--... Add lastRunTime, nextRunTime, and error fields similarly for TaskStatus ...-->

        <!-- Task Metadata -->
        <!--... Add createdBy, createdOn, lastModified, tags, and priority fields ...-->

        <!-- Task Log (Consider using a list and loop through logs) -->
        <!--... You might want a separate component or a modal for this, since logs can be many and detailed ...-->

        <!-- Task Payload -->
        <!--... Add apiKey, endpointUrl, filePath, parameters, and additionalConfig fields ...-->

        <div class="mt-6">
            <button @click="saveTask" class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
                {{ isEditing ? 'Save Changes' : 'Create Task' }}
            </button>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        isEditing: {
            type: Boolean,
            default: false
        },
        initialTask: {
            type: Object,
            default: () => ({})
        }
    },
    data() {
        return {
            task: this.initialTask
        }
    },
    methods: {
        saveTask() {
            if (this.isEditing) {
                // Handle edit logic
                this.$emit('updateTask', this.task);
            } else {
                // Handle creation logic
                this.$emit('createTask', this.task);
            }
        }
    }
}
</script>
