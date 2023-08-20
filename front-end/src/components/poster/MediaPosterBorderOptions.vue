<template>
  <div class="p-4 border rounded shadow">
    <h3 class="text-xl mb-4 font-semibold">Border Options</h3>

    <!-- Width Input -->
<!--    <div class="mb-4">
      <label class="block mb-1 font-medium" for="borderWidth">Width:</label>
      <input v-model.number="border.width" id="borderWidth" class="w-full px-3 py-2 border rounded" type="number">
    </div>-->
      <!-- Width Input -->
<!--    <div class="mb-4">-->
<!--      <label class="block mb-1 font-medium" for="borderHeight">Height:</label>-->
<!--      <input v-model.number="border.height" id="borderHeight" class="w-full px-3 py-2 border rounded" type="number">-->
<!--    </div>-->

    <!-- Color Input -->
    <div class="mb-4">
      <label class="block mb-1 font-medium" for="borderColor">Color:</label>
      <input v-model="border.color" id="borderColor" class="w-full px-3 py-2 border rounded" type="color">
    </div>

    <!-- Style Select -->
    <div>
      <label class="block mb-1 font-medium" for="borderStyle">Style:</label>
      <select  id="borderStyle" class="w-full px-3 py-2 border rounded">
        <option value="solid">Solid</option>
        <option value="dashed">Dashed</option>
        <option value="dotted">Dotted</option>
        <option value="double">Double</option>
        <!-- Add other styles as needed -->
      </select>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, PropType } from 'vue';
import { MediaPosterBorderOptions } from '@/models'; // Import your models here

export default defineComponent({
  name: 'MediaPosterBorderOptions',
  props: {
    value: { type: Object as PropType<MediaPosterBorderOptions>, required: true },
  },
  setup(props) {
    console.log(props.value)
    const border = ref(props.value);


    console.log(border.value);
    // Watch for changes in the props and update the local border options
    watch(
        () => props.value,
        (newValue) => {
          console.log('new value', newValue);
          border.value = newValue;
        }
    );

    return {
      border,
    };
  },
});
</script>

<style scoped>
/* Optional additional styling */
</style>
