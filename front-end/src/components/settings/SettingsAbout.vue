<template>
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


<script lang="ts">

export default {
    name: 'SettingsAbout',
    components: {},

    setup() {

        return {

        };
    }
};
</script>
