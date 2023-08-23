<template>
  <div class="p-3 border rounded shadow">

    <div class="mb-3">
<!--        <VCheckbox v-model="gradientOptions.enabled" class="mr-2" label="Enable" />-->
      <VToggle v-model="gradientOptions.enabled" class="mr-2" label="Enable" />
    </div>

    <div v-if="gradientOptions.enabled">
      <div class="mb-3">
        <label class="block mb-1">Gradient Colors:</label>
        <div v-for="(color, index) in gradientOptions.colors" :key="index">
          <div class="flex items-center">
            <Picker
                  v-if="gradientOptions.colors"
                  :pure-color="colorTupleToRGBString(color)"
                  @update:pure-color="(color) => handleColorChange(color, index)"
                  class="mr-2" />
<!--            <VInput type="color" v-model="gradientOptions.colors[index]" class="mr-2" />-->
            <VButton @click="removeColor(index)" label="Remove" class="text-red-500 hover:text-red-700"/>
          </div>
        </div>
        <VButton @click="addColor" label="Add Color" class="mt-2 text-blue-500 hover:text-blue-700" />
      </div>

      <div class="mb-3">
        <label class="block mb-1">Opacity:</label>
        <VSlider  min.number="0" max="1" step="0.1" v-model.number="gradientOptions.opacity"/>
        <span>{{ gradientOptions.opacity }}</span>
      </div>

      <div class="mb-3">
        <VSelect options="linear,radial" v-model="gradientOptions.type" label="Gradient Type:"/>
      </div>

      <div class="mb-3">
        <VSlider min.number=-180 max.number=180 step.number=1 v-model.number="gradientOptions.angle" class="border rounded p-1" label="Angle:" label-position="top"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watch } from 'vue';
import {MediaPosterGradientOptions, Color} from "@/models";
import VInput from "@/components/poster/MediaPosterBackgroundOptions.vue";
import VSlider from "@/components/ui/inputs/Slider.vue";
import VButton from "@/components/ui/inputs/Button.vue";
import VSelect from "@/components/ui/inputs/Select.vue";
import VCheckbox from "@/components/ui/inputs/Checkbox.vue";
import VToggle from "@/components/ui/inputs/Toggle.vue";
import {usePosterStore} from "@/store/posterStore";
import {ColorPicker as Picker} from "vue3-colorpicker";
import {validateColors} from "@/utils/arrays";
import debounce from 'lodash.debounce';
import {colorTupleToRGBString, parseRGB} from '@/utils/string';


export default defineComponent({
  name: 'MediaPosterGradientOptions',
  components: {Picker, VToggle, VCheckbox, VSelect, VButton, VSlider, VInput},
  props: {
    gradientOptions: {
      type: Object as PropType<MediaPosterGradientOptions>,
      required: true
    }
  },
  setup({gradientOptions}) {
      const posterStore = usePosterStore();

    const debouncedUpdate = debounce((newVal: MediaPosterGradientOptions) => {
      console.log('gradientOptions changed', newVal);
      // newVal.colors = validateColors(newVal.colors);
      posterStore.updateGradientOptions(newVal);
    }, 500); // 300 milliseconds debounce time

    watch(() => gradientOptions, (newVal, oldVal) => {
      console.log('gradientOptions changed', newVal)
      debouncedUpdate(newVal);
      // newVal.colors = validateColors(newVal.colors)
    }, { deep: true });
  },
  methods: {
    colorTupleToRGBString,
    addColor() {
      if(!this.gradientOptions.colors) {
        this.gradientOptions.colors = [];
      }

      if(this.gradientOptions.colors.length >= 6) {
        return;
      }

      this.gradientOptions.colors.push([255,255,255]); // Default to white color,
    },
    handleColorChange(color: string, index: number) {
      console.log(color,index)
      if(!this.gradientOptions.colors) {
        return;
      }
      console.log(color, index)
      this.gradientOptions.colors[index] = parseRGB(color)
    },
    removeColor(index: number) {
      if(!this.gradientOptions.colors) {
        return;
      }

      this.gradientOptions.colors.splice(index, 1);
    }
  }
});
</script>

<style scoped>
/* Optional additional styling */
label {
  display: block;
  margin-bottom: 10px;
}
</style>
