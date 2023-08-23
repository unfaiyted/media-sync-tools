<template>
  <div class="p-2">

    <div class="" v-if="options.enabled">
      <div class="flex items-center space-x-2">
        <VInput v-model="options.text" class="w-full  py-2 " label="Text:" />
        <div class="pt-2">
          <ColorPicker
              :pure-color="colorTupleToRGBString(options.color)"
              @update:pure-color="(color) => handleColorChange(color)" id="borderColor" />

        </div>
      </div>
    </div>

    <!-- Border Options -->
    <media-poster-border-options v-if="options.enabled" v-model="options.border"  :border="options.border" parent="text"/>

    <!-- Shadow Options -->
    <media-poster-shadow-options v-if="options.enabled" v-model="options.shadow" class="mt-4" />

    <!-- Position Inputs -->
    <div class="mb-3 border rounded mt-4 p-2" v-if="options.enabled">
      <label class="block mb-1 font-bold">Offset Position:</label>
      <div class="flex space-x-2">
        <VSlider v-model:number="options.position[0]" class="w-1/2 px-3 py-2 " label="X" label-position="left"/>
        <VSlider v-model:number="options.position[1]" class="w-1/2 px-3 py-2 " label="Y" label-position="left"/>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { ref, defineComponent, watch, PropType } from 'vue';
import { MediaPosterTextOptions } from '@/models'; // Import your models here
import MediaPosterBorderOptions from './MediaPosterBorderOptions.vue'; // Assuming you have separate components for each option
import MediaPosterShadowOptions from './MediaPosterShadowOptions.vue';
import VInput from "@/components/ui/inputs/Input.vue";
import VCheckbox from "@/components/ui/inputs/Checkbox.vue";
import {ColorPicker} from "vue3-colorpicker";
import VSlider from "@/components/ui/inputs/Slider.vue";
import {usePosterStore} from "@/store/posterStore";
import {colorTupleToRGBString, parseRGB} from "@/utils/string";

export default defineComponent({
  name: 'MediaPosterTextOptions',
  methods: {colorTupleToRGBString},
  components: {VSlider, ColorPicker, VCheckbox, VInput, MediaPosterBorderOptions, MediaPosterShadowOptions },
  props: {
    value: { type: Object as PropType<MediaPosterTextOptions>, required: true },
  },
  setup(props) {
    const options = ref(props.value);
    const posterStore = usePosterStore();

    const handleColorChange = (color: string) => {
      if(!options.value.color) {
        return;
      }
      console.log('changing color')
      options.value.color = parseRGB(color)
    }


    // Watch for changes in the props and update the local options
    watch(props.value,
        (newValue) => {
          options.value = newValue;
          console.log('text options changed', newValue)
          posterStore.updateTextOptions(newValue);
        }
    );

    return {
      options,
      handleColorChange
    };
  },
});
</script>

<style scoped>
/* Optional additional styling */
</style>
