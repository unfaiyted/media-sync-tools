<template>
  <div class="p-2 rounded border">
    <h4 class="text-md font-bold">Border Options</h4>
<!--     Width Input -->


      <div class="flex space-x-2 w-full">
        <VSlider v-model.number="border.width" max="10" class=" w-1/2 px-3 py-2 " label="Width" />
        <VSlider v-model.number="border.height" max="10" class="w-1/2 px-3 py-2 " label="Height" />
      </div>

    <!-- Color Input -->
    <div class="mb-4 flex">
      <div class="mt-2">
        <label class="block mb-1 font-medium" for="borderColor">Color:</label>
        <ColorPicker
            :pure-color="colorTupleToRGBString(border.color)"
            @update:pure-color="(color) => handleColorChange(color)" id="borderColor" />


      </div>
<!--      <VSelect label="Style:" options="solid,dashed,dotted,double" v-model="border.style" id="borderStyle" class="w-full px-3 py-2" />-->
    </div>

    <!-- Style Select -->
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, PropType } from 'vue';
import {MediaPosterBorderOptions, MediaPosterGradientOptions, MediaPosterTextOptions} from '@/models';
import VSelect from "@/components/ui/inputs/Select.vue";
import {ColorPicker} from "vue3-colorpicker";
import VSlider from "@/components/ui/inputs/Slider.vue";
import {colorTupleToRGBString, parseRGB} from "@/utils/string";
import debounce from "lodash.debounce"; // Import your models here
import {usePosterStore} from "@/store/posterStore";

export default defineComponent({
  name: 'MediaPosterBorderOptions',
  methods: {colorTupleToRGBString},
  components: {VSlider, ColorPicker, VSelect},
  props: {
    border: { type: Object as PropType<MediaPosterBorderOptions>, required: true },
    parent: {
      type: String,
      required: false
    }
  },
  setup({border, parent}) {
    const borderOptions = ref<MediaPosterBorderOptions>(border);
    const store = usePosterStore();

    const handleColorChange = (color: string) => {
      if(!borderOptions.value.color) {
        return;
      }
      borderOptions.value.color = parseRGB(color)
    }



    console.log(borderOptions.value);

    const debouncedUpdate = debounce((newVal: MediaPosterBorderOptions) => {
      console.log('gradientOptions changed', newVal);
      // newVal.colors = validateColors(newVal.colors);

      if(parent === 'text') {
        store.updateTextBorderOptions(newVal);
      } else {
        store.updateBorderOptions(newVal);
      }


    }, 500); // 300 milliseconds debounce time


    // Watch for changes in the props and update the local border options
    watch(
        () => border ,
        (newValue) => {
          console.log('border changed', newValue);

         debouncedUpdate(newValue);
        }, {deep: true}
    );

    return {
      border,
      handleColorChange
    };
  },
});
</script>

<style scoped>
/* Optional additional styling */
</style>
