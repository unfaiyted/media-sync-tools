<template>
  <div class="p-4 border rounded shadow">
    <h3 class="text-xl mb-4 font-semibold">Gradient Options</h3>

    <div class="mb-3">
      <label class="flex items-center">
        <input type="checkbox" v-model="gradientOptions.enabled" class="mr-2">
        Enable Gradient
      </label>
    </div>

    <div v-if="gradientOptions.enabled">
      <div class="mb-3">
        <label class="block mb-1">Gradient Colors:</label>
        <div v-for="(color, index) in gradientOptions.colors" :key="index">
          <div class="flex items-center">
            <input type="color" v-model="gradientOptions.colors[index]" class="mr-2">
            <button @click="removeColor(index)" class="text-red-500 hover:text-red-700">Remove</button>
          </div>
        </div>
        <button @click="addColor" class="mt-2 text-blue-500 hover:text-blue-700">Add Color</button>
      </div>

      <div class="mb-3">
        <label class="block mb-1">Opacity:</label>
        <input type="range" min="0" max="1" step="0.1" v-model.number="gradientOptions.opacity">
        <span>{{ gradientOptions.opacity }}</span>
      </div>

      <div class="mb-3">
        <label class="block mb-1">Gradient Type:</label>
        <select v-model="gradientOptions.type">
          <option value="linear">Linear</option>
          <option value="radial">Radial</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="block mb-1">Angle:</label>
        <input type="number" v-model.number="gradientOptions.angle" class="border rounded p-1">
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';
import {MediaPosterGradientOptions} from "@/models";



export default defineComponent({
  name: 'MediaPosterGradientOptions',
  props: {
    gradientOptions: {
      type: Object as PropType<MediaPosterGradientOptions>,
      required: true
    }
  },
  methods: {
    addColor() {
      this.gradientOptions.colors.push('#FFFFFF'); // Default to white color, adjust if needed
    },
    removeColor(index: number) {
      this.gradientOptions.colors.splice(index, 1);
    }
  }
});
</script>

<style scoped>
/* Optional additional styling */
</style>
