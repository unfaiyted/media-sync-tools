<template>
  <div class="bg-gray-100 p-6">
    <h1 class="text-2xl font-semibold mb-4">List Viewer</h1>

    <!-- Search and Fetch Section -->
    <div class="mb-4 flex items-center">
      <label for="idType" class="mr-2">ID Type:</label>
      <select v-model="selectedIdType" id="idType" class="border p-2 rounded w-40 mr-4">
        <option v-for="type in idTypes" :key="type">{{ type }}</option>
      </select>

      <label for="idSearch" class="mr-2">ID:</label>
      <input v-model="searchId" id="idSearch" type="text" class="border p-2 rounded w-40 mr-4">

      <button @click="fetchList" class="bg-blue-500 text-white px-4 py-2 rounded">Fetch</button>
    </div>

    <!-- List Table -->
    <table class="min-w-full bg-white border rounded shadow">
      <!-- ... rest of the table ... -->
    </table>

    <!-- ... rest of the code ... -->
  </div>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      selectedIdType: '',
      localItems: [...this.items], // Initialize localItems with items prop
      searchId: '',
      idTypes: ['emby', 'plex', 'trakt', 'imdb'],
      // ... other data properties ...
    };
  },
  watch: {
    // Watch for changes to the items prop and update localItems when it changes
    items(newItems) {
      this.localItems = [...newItems];
    }
  },
  methods: {
    async fetchList() {
      if (this.selectedIdType && this.searchId) {
        const apiUrl = `http://localhost:3000/lists/${this.selectedIdType}/${this.searchId}`;

        try {
          const response = await fetch(apiUrl);
          const data = await response.json();

          if (data && data.items) {
            this.localItems = data.items; // Use localItems here
          } else {
            console.error('No list data returned');
          }
        } catch (error) {
          console.error('Error fetching list:', error);
        }
      } else {
        alert('Please select an ID Type and enter an ID.');
      }
    },
    // ... other methods ...
  }
}
</script>
