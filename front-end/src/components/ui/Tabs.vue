<template>
  <div>
    <!-- Tabs Header -->
    <div class="flex border-b">
      <div v-for="(tab, index) in tabs">
        <button
            :key="tab.title"
            class="px-4 py-2"
            :class="{ 'border-b-2 border-blue-500': isActiveTab(index) }"
            @click="setActiveTab(index)"
        >
          {{ tab.title }}
        </button>
      </div>
    </div>

    <!-- Tabs Content -->
    <div class="mt-4">
      <div v-for="(tab, index) in tabs" >
        <div v-if="isActiveTab(index)" class="p3">
          <slot :name="tab.title"></slot>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TabComponent",
  props: {
    tabs: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  data() {
    return {
      activeTabIndex: 0
    };
  },
  methods: {
    setActiveTab(index) {
      console.log('index', index)
      this.activeTabIndex = index;
    },
    isActiveTab(index) {
      console.log('index', index, this.activeTabIndex)
      return this.activeTabIndex === index;
    }
  }
};
</script>

<style scoped>
/* Tailwind CSS styles can be customized if needed */
</style>
