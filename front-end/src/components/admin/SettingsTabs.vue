<template>
  <Tabs :tabs="tabsList">

    <template v-slot:General>
      <div class="space-y-4">
        <label class="block">
          API Key:
          <input class="block w-full mt-1 p-2 border rounded" type="text" placeholder="Your API Key here">
        </label>
        <label class="block">
          Title:
          <input class="block w-full mt-1 p-2 border rounded" type="text" placeholder="Your title here">
        </label>
        <label class="block">
          URL:
          <input class="block w-full mt-1 p-2 border rounded" type="text" placeholder="https://example.com">
        </label>
        <label class="block">
          Display Language:
          <select class="block w-full mt-1 p-2 border rounded">
            <option>English</option>
            <option>Spanish</option>
            <!-- Add more languages here -->
          </select>
        </label>
      </div>
    </template>
    <template v-slot:User>
      <div class="space-y-4">
        <label class="block">
          Enable remote access:
          <input type="checkbox" class="ml-2">
        </label>

        <div class="space-y-2">
          <div class="font-semibold">Default Permissions:</div>
          <label><input type="checkbox" class="mr-2">Create Lists</label>
          <label><input type="checkbox" class="mr-2">Edit Lists</label>
          <label><input type="checkbox" class="mr-2">Delete Lists</label>
          <label><input type="checkbox" class="mr-2">Create Users</label>
          <label><input type="checkbox" class="mr-2">Can edit providers</label>
          <!-- ... other permissions ... -->
        </div>
      </div>
    </template>

    <template v-slot:Providers>
    <SettingsProviders />
    </template>

    <template v-slot:Logs>
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
    </template>

    <template v-slot:Tasks>
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
    </template>


    <template v-slot:About>
      <div class="space-y-4">
        <div>
          <strong>Version:</strong> 1.0.0
        </div>
        <div>
          <strong>License:</strong> MIT
        </div>
        <div>
          <strong>Github:</strong> <a href="#" class="text-blue-500 underline hover:text-blue-700">Link to repo</a>
        </div>
        <div>
          <strong>Docker:</strong> <a href="#" class="text-blue-500 underline hover:text-blue-700">DockerHub Link</a>
        </div>
        <div>
          <strong>Support:</strong> <a href="#" class="text-blue-500 underline hover:text-blue-700">Support Forum</a>
        </div>
        <div>
          <strong>Donate:</strong> <a href="#" class="text-blue-500 underline hover:text-blue-700">Donation Page</a>
        </div>

        <div class="p-4 border rounded shadow space-y-2">
          <h2 class="text-lg font-bold">Release History</h2>
          <ul class="list-disc pl-5 space-y-2">
            <li>
              <strong>1.0.0:</strong> Initial release.
            </li>
            <li>
              <strong>0.9.0-beta:</strong> Beta testing phase.
            </li>
            <!-- Add more release notes as needed -->
          </ul>
        </div>

        <div class="p-4 border rounded shadow space-y-2">
          <h2 class="text-lg font-bold">Changelog</h2>
          <ul class="list-disc pl-5 space-y-2">
            <li>
              <strong>1.0.0:</strong>
              <ul class="list-disc pl-5">
                <li>Added feature X.</li>
                <li>Fixed bug Y.</li>
                <!-- More changelog items -->
              </ul>
            </li>
            <li>
              <strong>0.9.0-beta:</strong>
              <ul class="list-disc pl-5">
                <li>Implemented alpha features.</li>
                <!-- More changelog items -->
              </ul>
            </li>
            <!-- Add more changelog notes as needed -->
          </ul>
        </div>
      </div>
    </template>
  </Tabs>
</template>

<script>
import Tabs from "@/components/ui/Tabs.vue";
import SettingsProviders  from "@/components/admin/SettingsProviders.vue";

export default {
  components: {
   Tabs
  },
  data() {
    return {
      tabsList: [
        { title: "General" },
        { title: "User" },
        { title: "Providers" },
        { title: "Lists" },
        { title: "Logs" },
        { title: "Tasks" },
        { title: "About" }
      ]
    };
  }
};
</script>
