<template>
  <div :class="{ 'w-64': !isCollapsed, 'w-20': isCollapsed }" class="bg-gray-900 text-white min-h-screen px-4 py-6 space-y-4 transition-all duration-300">
    <router-link class="block py-2 px-3 rounded hover:bg-gray-700" to="/">Dashboard</router-link>
    <router-link class="block py-2 px-3 rounded hover:bg-gray-700" to="/poster">Posters</router-link>
<!--    <router-link class="block py-2 px-3 rounded hover:bg-gray-700" to="/merge-lists">Merge Lists</router-link>-->
    <router-link class="block py-2 px-3 rounded hover:bg-gray-700" to="/settings">Settings</router-link>
    <router-link class="block py-2 px-3 rounded hover:bg-gray-700" to="/tools">Tools</router-link>
    <router-link class="block py-2 px-3 rounded hover:bg-gray-700" to="/about">About</router-link>
      <router-link class="block py-2 px-3 rounded hover:bg-gray-700" to="/admin">Admin</router-link>
    <!-- Content remains the same -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      isCollapsed: false
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
    }
  }
}
</script>
