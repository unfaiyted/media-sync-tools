<template>
      <div class="p-3 border rounded ">
        <h4 class="text-md mb-4 font-semibold">Shadow Options</h4>
          <VSlider id="shadowOffsetX"
                   label="Offset X:"
                   v-model="shadow.offsetX" type="number" placeholder="Enter shadow X offset"/>
            <VSlider id="shadowOffsetY"
                     label="Offset Y:"
                     v-model="shadow.offsetY" type="number" placeholder="Enter shadow Y offset" />
            <VSlider id="shadowBlur" v-model="shadow.blur" type="number" placeholder="Enter shadow blur"
            label="Blur:"/>
<!--            <VSlider id="shadowColor" v-model="shadow.color" type="color" placeholder="Select shadow color" label="Shadow:"/>-->
            <ColorPicker/>
    </div>
</template>

<script>
import VInput from "@/components/poster/MediaPosterBackgroundOptions.vue";
import VSlider from "@/components/ui/inputs/Slider.vue";
import {ColorPicker} from "vue3-colorpicker";

export default {
    name: "MediaPosterShadowOptions",
  components: {ColorPicker, VSlider, VInput},
    data() {
        return {
            shadow: {
                offsetX: 0,  // Default X offset
                offsetY: 0,  // Default Y offset
                blur: 5, // Default blur
                color: [0,0,0], // Default color
            }
        };
    }
};
</script>

<style scoped>
/* You can add any specific styles for this component here */
</style>
