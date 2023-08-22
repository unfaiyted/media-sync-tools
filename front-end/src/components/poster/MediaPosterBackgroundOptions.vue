<template>
  <div class="p-4 border rounded shadow">
    <h3 class="text-xl mb-4 font-semibold">Background Options</h3>

    <div class="mb-3">
        <VCheckbox
            label="Enable Background"
            label-position="right"
            v-model="backgroundOptions.enabled" class="mr-2">
        </VCheckbox>
    </div>

    <div v-if="backgroundOptions.enabled">
      <div class="mb-3">
        <label class="block mb-1">Background URL:</label>
        <input type="text" v-model="backgroundOptions.url" class="border rounded p-1 w-full">
      </div>

      <div class="mb-3">
        <label class="block mb-1">Background Color:</label>
        <input type="color" v-model="backgroundOptions.color" class="mr-2">
      </div>

<!--      <div class="mb-3">
        <label class="block mb-1">Position:</label>
        <div class="flex">
          <input type="number" v-model.number="backgroundOptions.position[0]" class="border rounded p-1 w-1/2 mr-2" placeholder="X">
          <input type="number" v-model.number="backgroundOptions.position[1]" class="border rounded p-1 w-1/2" placeholder="Y">
        </div>
      </div-->>

<!--      <div class="mb-3">
        <label class="block mb-1">Size:</label>
        <div class="flex">
          <input type="number" v-model.number="backgroundOptions.size[0]" class="border rounded p-1 w-1/2 mr-2" placeholder="Width">
          <input type="number" v-model.number="backgroundOptions.size[1]" class="border rounded p-1 w-1/2" placeholder="Height">
        </div>
      </div>-->

      <div class="mb-3">
        <label class="block mb-1">Opacity:</label>
        <input type="range" min="0" max="1" step="0.1" v-model.number="backgroundOptions.opacity">
        <span>{{ backgroundOptions.opacity }}</span>
      </div>

      <!-- Additional fields can be added here similarly -->
      <!-- Border Options -->
      <media-poster-border-options v-if="backgroundOptions.enabled" v-model="backgroundOptions.border" :value="backgroundOptions.border" />

      <!-- Shadow Options -->
      <media-poster-shadow-options v-if="backgroundOptions.enabled" v-model="backgroundOptions.shadow" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import { MediaPosterBackgroundOptions } from "@/models";
import MediaPosterBorderOptions from "@/components/poster/MediaPosterBorderOptions.vue";
import MediaPosterShadowOptions from "@/components/poster/MediaPosterShadowOptions.vue";
import VCheckbox from "@/components/ui/inputs/Checkbox.vue";

export default defineComponent({
  name: 'MediaPosterBackgroundOptions',
  components: {VCheckbox, MediaPosterShadowOptions, MediaPosterBorderOptions},
  props: {
    backgroundOptions: {
      type: Object as PropType<MediaPosterBackgroundOptions>,
      required: true
    }
  },
});
</script>

<style scoped>
/* Optional additional styling */
</style>
