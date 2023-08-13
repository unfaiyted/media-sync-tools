<template>
  <div class="bg-gray-100 p-6">
    <h1 class="text-2xl font-semibold mb-4">List Viewer</h1>

    <table class="min-w-full bg-white border rounded shadow">
      <thead>
      <tr>
        <th class="border px-4 py-2">Item Name</th>
        <th class="border px-4 py-2">Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="item in listItems" :key="item.id">
        <td class="border px-4 py-2">{{ item.name }}</td>
        <td class="border px-4 py-2">
          <button @click="showPopover(item)" class="bg-blue-500 text-white px-4 py-2 rounded shadow mr-2">Options</button>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- Popover -->
    <div v-if="popoverVisible" class="fixed top-0 left-0 w-full h-full flex items-center justify-center">
      <div class="bg-white p-4 rounded shadow-lg w-1/3">
        <h2 class="text-lg font-semibold mb-4">Actions for {{ currentItem.name }}</h2>
        <button class="block mb-2">Edit</button>
        <button class="block mb-2">Delete</button>
        <button class="block mb-2">Copy to...</button>
      </div>
    </div>

    <!-- Buttons to sync lists -->
    <div class="mt-4">
      <button class="bg-green-500 text-white px-4 py-2 rounded shadow mr-2">Sync to Trakt</button>
      <button class="bg-green-500 text-white px-4 py-2 rounded shadow">Sync to Emby</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      popoverVisible: false,
      currentItem: {}
    }
  },
  methods: {
    showPopover(item) {
      this.popoverVisible = true;
      this.currentItem = item;
    },
    // You can add more methods to handle edit, delete, copy, etc.
  }
}
</script>
