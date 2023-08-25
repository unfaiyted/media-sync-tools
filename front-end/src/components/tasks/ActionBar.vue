<template>
    <div class="flex items-center justify-between bg-gray-100 p-4 border-t border-gray-300">
        <button @click="goBack" class="text-gray-600 hover:text-gray-800">
            <i class="fas fa-arrow-left"></i> Back to List
        </button>

        <div class="space-x-4">
            <button @click="triggerTask" class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:ring-2 focus:ring-blue-400">Run Now</button>
            <button @click="saveTask" class="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:ring-2 focus:ring-green-400">Save</button>
            <button @click="deleteTask" class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:ring-2 focus:ring-red-400">Delete</button>
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
    methods: {
        goBack() {
            this.$router.push({ name: 'TaskList' }); // Assuming you named the route 'TaskList'
        },
        triggerTask() {
            // You can use the API call for triggering the task here
            this.$emit('triggerTask', this.task);
        },
        saveTask() {
            // Handle saving the task (either create or edit)
            this.$emit('saveTask', this.task);
        },
        deleteTask() {
            // Handle deletion after confirmation
            if (confirm("Are you sure you want to delete this task?")) {
                this.$emit('deleteTask', this.task);
            }
        }
    }
}
</script>
