<template>
  <div>
    <!-- Enabled Checkbox -->
    <label class="mb-2 flex items-center">
      <input type="checkbox" v-model="options.enabled" class="mr-2">
      Enable Text Options
    </label>

    <!-- Text Input -->
    <div class="mb-4" v-if="options.enabled">
      <label class="block mb-1 font-medium">Text:</label>
      <input v-model="options.text" class="w-full px-3 py-2 border rounded">
    </div>

    <!-- Position Inputs -->
    <div class="mb-4" v-if="options.enabled">
      <label class="block mb-1 font-medium">Position:</label>
      <div class="flex space-x-2">
        <input v-model="options.position[0]" class="w-1/2 px-3 py-2 border rounded" placeholder="X">
        <input v-model="options.position[1]" class="w-1/2 px-3 py-2 border rounded" placeholder="Y">
      </div>
    </div>

    <!-- Color Input -->
    <div class="mb-4" v-if="options.enabled">
      <label class="block mb-1 font-medium">Color:</label>
      <div class="flex space-x-2">
        <input v-model="options.color[0]" class="w-1/3 px-3 py-2 border rounded" placeholder="R">
        <input v-model="options.color[1]" class="w-1/3 px-3 py-2 border rounded" placeholder="G">
        <input v-model="options.color[2]" class="w-1/3 px-3 py-2 border rounded" placeholder="B">
      </div>
    </div>

    <!-- Border Options -->
    <media-poster-border-options v-if="options.enabled" v-model="options.border" />

    <!-- Shadow Options -->
    <media-poster-shadow-options v-if="options.enabled" v-model="options.shadow" />
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, watch } from 'vue';
import { MediaPosterTextOptions } from '../../models'; // Import your models here
import MediaPosterBorderOptions from './MediaPosterBorderOptions.vue'; // Assuming you have separate components for each option
import MediaPosterShadowOptions from './MediaPosterShadowOptions.vue';

export default defineComponent({
  name: 'MediaPosterTextOptions',
  components: { MediaPosterBorderOptions, MediaPosterShadowOptions },
  props: {
    value: { type: Object as () => MediaPosterTextOptions, required: true },
},
setup(props) {
  const options = ref(props.value);

  // Watch for changes in the props and update the local options
  watch(
      () => props.value,
      (newValue) => {
        options.value = newValue;
      }
  );

  return {
    options,
  };
},
});
</scriptt>
