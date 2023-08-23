<template>
  <div class="p-2">



    <div class="" >
      <div class="flex items-center space-x-2">
        <VInput v-model="options.url" class="w-full  py-2 " label="Url:" />
        <div class="pt-2">

        </div>
      </div>
    </div>

    <DragDrop/>
    <!-- Position Inputs -->
    <div class="mb-3 border rounded mt-4 p-2">
      <label class="block mb-1 font-bold">Offset Position:</label>
      <div class="flex space-x-2" v-if="options.position" >
        <VSlider v-model:number="options.position[0]" class="w-1/2 px-3 py-2 " icon="ArrowsUpDownIcon" label-position="left"/>
        <VSlider v-model:number="options.position[1]" class="w-1/2 px-3 py-2 " icon="ArrowsRightLeftIcon" label-position="left"/>
      </div>
    </div>

    <div class="mb-3">
      <label class="block mb-1">Opacity:</label>
      <VSlider  :min="0" :max="1" :step="0.1" v-model.number="options.opacity"/>
      <span>{{ options.opacity }}</span>
    </div>

  <div class="" >
      <div class="flex items-center space-x-2" v-if="backgroundImages">
        <VSelect :options="backgroundImages" v-model="options.url" class="w-full  py-2 " label="Image:" />
        <div class="pt-2">

        </div>
      </div>
    </div>
  </div>
</template>



<script lang="ts">
import { ref, defineComponent, watch, onBeforeMount } from 'vue';
import { MediaPosterBackgroundOptions } from '@/models';
import VInput from "@/components/ui/inputs/Input.vue";
import VSlider from "@/components/ui/inputs/Slider.vue";
import { usePosterStore } from "@/store/posterStore";
import VSelect from "@/components/ui/inputs/Select.vue";

export interface FileOption {
      text: string;
      value: string;
    }

export default defineComponent({
  name: 'MediaPosterBackgroundOptions',
  components: {VSelect, VSlider, VInput, },

  props: {
    value: { type: Object as PropType<MediaPosterBackgroundOptions>, required: true },
  },

  setup(props) {
    const options = ref(props.value);
    const posterStore = usePosterStore();
    const backgroundImages = ref<FileOption[]>();

    onBeforeMount(async () => {
      backgroundImages.value = await posterStore.getBackgroundImages();
    });


    watch(options, (newValue) => {
      console.log('backgroundOptions changed', newValue)
      posterStore.updateBackgroundOptions(newValue);
    });

  /*  watch(() => props.value, (newValue) => {
      options.value = newValue;
      console.log('backgroundOptions changed', newValue)
      posterStore.updateBackgroundOptions(newValue);
    });
*/
    return {
      options,
      backgroundImages
    };
  },
});
</script>

<style scoped>
/* Optional additional styling */
</style>
