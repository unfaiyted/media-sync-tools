<template>
  <div class="p-4 border rounded shadow">
    <h3 class="text-xl mb-4 font-semibold">Overlay Options</h3>

    <!-- Add Overlay Button -->
    <button @click="addOverlay" class="mb-4 bg-blue-500 text-white px-3 py-2 rounded hover:bg-blue-600">
      Add Overlay
    </button>

    <!-- Overlay Options List -->
    <div v-for="(overlay, index) in options" :key="index" class="mb-6">
      <div class="flex items-center mb-2">
        <span class="text-lg font-semibold">Overlay {{ index + 1 }}</span>
        <button @click="removeOverlay(index)" class="ml-auto text-red-500 hover:text-red-700">
          Remove
        </button>
      </div>

      <!-- Enabled Checkbox -->
      <div class="mb-2">
        <label class="flex items-center">
          <input type="checkbox" v-model="overlay.enabled" class="mr-2">
          Enable Overlay
        </label>
      </div>

      <!-- Text Input -->
      <div class="mb-4" v-if="overlay.enabled">
        <label class="block mb-1 font-medium">Text:</label>
        <input v-model="overlay.text" class="w-full px-3 py-2 border rounded">
      </div>

      <!-- Position Input -->
      <div class="mb-4" v-if="overlay.enabled">
        <label class="block mb-1 font-medium">Position:</label>
        <input v-model="overlay.position" class="w-full px-3 py-2 border rounded">
      </div>

      <!-- Text Color Input -->
      <div class="mb-4" v-if="overlay.enabled">
        <label class="block mb-1 font-medium">Text Color:</label>
        <div class="flex space-x-2">
<!--          <input v-model="overlay.textColor[0]" class="w-1/3 px-3 py-2 border rounded" placeholder="R">-->
<!--          <input v-model="overlay.textColor[1]" class="w-1/3 px-3 py-2 border rounded" placeholder="G">-->
<!--          <input v-model="overlay.textColor[2]" class="w-1/3 px-3 py-2 border rounded" placeholder="B">-->
        </div>
      </div>

      <!-- Background Color Input -->
      <div class="mb-4" v-if="overlay.enabled">
        <label class="block mb-1 font-medium">Background Color:</label>
        <div class="flex space-x-2">
<!--          <input v-model="overlay.backgroundColor[0]" class="w-1/3 px-3 py-2 border rounded" placeholder="R">-->
<!--          <input v-model="overlay.backgroundColor[1]" class="w-1/3 px-3 py-2 border rounded" placeholder="G">-->
<!--          <input v-model="overlay.backgroundColor[2]" class="w-1/3 px-3 py-2 border rounded" placeholder="B">-->
        </div>
      </div>

      <!-- Transparency Input -->
      <div class="mb-4" v-if="overlay.enabled">
        <label class="block mb-1 font-medium">Transparency:</label>
        <input type="range" min="0" max="100" v-model.number="overlay.transparency">
        <span>{{ overlay.transparency }}</span>
      </div>

      <!-- Corner Radius Input -->
      <div class="mb-4" v-if="overlay.enabled">
        <label class="block mb-1 font-medium">Corner Radius:</label>
        <input type="number" v-model.number="overlay.cornerRadius" class="w-full px-3 py-2 border rounded">
      </div>

      <!-- Icon Options -->
      <media-poster-icon-options v-if="overlay?.icon?.enabled" v-model="overlay.icon"  :icon-options="overlay.icon"/>

      <!-- Border Options -->
      <media-poster-border-options v-if="overlay?.border?.enabled" v-model="overlay.border" :value="overlay.border"/>

      <!-- Shadow Options -->
      <media-poster-shadow-options v-if="overlay?.shadow?.enabled" v-model="overlay.shadow" />
    </div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, watch, PropType } from 'vue';
import {IconPosition, MediaPosterOverlayOptions} from '@/models'; // Import your models here
import MediaPosterIconOptions from './MediaPosterIconOptions.vue'; // Assuming you have a component for icon options
import MediaPosterBorderOptions from './MediaPosterBorderOptions.vue'; // Assuming you have a component for border options
import MediaPosterShadowOptions from './MediaPosterShadowOptions.vue'; // Assuming you have a component for shadow options

export default defineComponent({
  name: 'MediaPosterOverlayOptions',
  components: { MediaPosterIconOptions, MediaPosterBorderOptions, MediaPosterShadowOptions },
  props: {
    overlayOptions: { type: Object as PropType<Array<MediaPosterOverlayOptions>>, required: true },
  },
  setup(props) {
    const options = ref<Array<MediaPosterOverlayOptions>>(props.overlayOptions);

    // Watch for changes in the props and update the local options
    watch(
        () => props.overlayOptions,
        (newValue) => {
          options.value = newValue;
        }
    );

    // Add a new overlay
    function addOverlay() {
      options.value.push({
        enabled: false,
        cornerRadius: 0,
        transparency: 0,
        icon: {
          enabled: false,
          path: '',
          size: [0, 0],
          position: IconPosition.LEFT,
        },
        position: IconPosition.LEFT // Default position, adjust if needed
      });
    }

    // Remove an overlay by index
    function removeOverlay(index: number) {
      options.value.splice(index, 1);
    }

    return {
      options,
      addOverlay,
      removeOverlay,
    };
  },
});
</script>

<style scoped>
/* Optional additional styling */
</style>
