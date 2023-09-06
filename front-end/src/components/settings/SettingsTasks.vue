<template>
  <div class="space-y-4">

    <div class="space-y-2">
    </div>
    <div class="space-y-4">
      <div class="flex space-x-4">
        <button class="bg-blue-500 text-white p-2 rounded">Add Task</button>
      </div>

      <!-- Example card for Tasks -->
      <div class="p-4 border rounded shadow space-y-2">
        <h2 class="text-lg font-bold">Task Name</h2>
        <p>Type: Cleanup</p>
        <p>Next run date: 2023-09-03</p>
        <div class="flex space-x-4">
          <button class="bg-blue-500 text-white p-2 rounded">Edit</button>
          <button class="bg-red-500 text-white p-2 rounded">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import UserManagement from "@/components/admin/UserManager.vue";

export default {
  name: 'SettingsTasks',
  components: {UserManagement},

  setup() {

    return {};
  }
};
</script>
