<template>
  <div class="p-4 border rounded shadow">
    <h3 class="text-xl mb-4 font-semibold">Icon Options</h3>

    <!-- Enabled Checkbox -->
    <label class="mb-2 flex items-center">
      <input type="checkbox" v-model="options.enabled" class="mr-2">
      Enable Icon Options
    </label>

    <!-- Icon Path Input -->
    <div class="mb-4" v-if="options.enabled">
      <label class="block mb-1 font-medium">Icon Path:</label>
      <input v-model="options.path" class="w-full px-3 py-2 border rounded">
    </div>

    <!-- Icon Position -->
    <div class="mb-4" v-if="options.enabled">
      <label class="block mb-1 font-medium">Icon Position:</label>
      <select v-model="options.position" class="w-full px-3 py-2 border rounded">
        <option value="LEFT">Left</option>
        <option value="MIDDLE">Middle</option>
        <option value="RIGHT">Right</option>
        <option value="TOP">Top</option>
        <option value="BOTTOM">Bottom</option>
      </select>
    </div>

    <!-- Icon Size Inputs -->
    <div class="mb-4" v-if="options.enabled">
      <label class="block mb-1 font-medium">Icon Size:</label>
      <div class="flex space-x-2">
        <input v-model="options.size[0]" class="w-1/2 px-3 py-2 border rounded" placeholder="Width">
        <input v-model="options.size[1]" class="w-1/2 px-3 py-2 border rounded" placeholder="Height">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, watch, PropType } from 'vue';
import { MediaPosterIconOptions, IconPosition } from '@/models'; // Import your models here

export default defineComponent({
  name: 'MediaPosterIconOptions',
  props: {
    iconOptions: { type: Object as PropType<MediaPosterIconOptions>, required: true },
  },
  setup(props) {
    const options = ref(props.iconOptions);

    // Watch for changes in the props and update the local options
    watch(
        () => props.iconOptions,
        (newValue) => {
          options.value = newValue;
        }
    );

    return {
      options,
      IconPosition, // Expose the enum to the template
    };
  },
});
</script>

<style scoped>
/* Optional additional styling */
</style>
