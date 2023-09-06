

<template>
    <div class="space-y-4">
        <label class="block">
            Enable remote access:
            <input type="checkbox" class="ml-2">
        </label>

      <div class="space-y-4">
        <label class="block">
          Log level:
          <select class="block w-full mt-1 p-2 border rounded">
            <option>Info</option>
            <option>Error</option>
            <option>Warning</option>
          </select>
        </label>
        <label class="block">
          Log file location:
          <input class="block w-full mt-1 p-2 border rounded" type="text" placeholder="/path/to/log/file">
        </label>
        <label class="block">
          Log file size:
          <input class="block w-full mt-1 p-2 border rounded" type="text" placeholder="5MB">
        </label>

        <!-- Log file viewer section -->
        <div class="p-4 border rounded shadow space-y-2">
          <h2 class="text-lg font-bold">Log File Viewer</h2>
          <textarea class="w-full h-32 p-2 border rounded" readonly></textarea>
          <button class="bg-blue-500 text-white p-2 rounded">Download Log</button>
        </div>
      </div>
    </div>
</template>


<script lang="ts">
import UserManagement from "@/components/admin/UserManager.vue";

export default {
    name: 'SettingsLogs',
    components: {UserManagement},

    setup() {

        return {

        };
    }
};
</script>
