<template>
    <div class="media-item-poster relative cursor-pointer hover:opacity-80" :style="mediaItem.poster && !imageError ? {} : randomGradient">
        <!-- Conditional Image Poster based on whether it's loaded successfully -->
        <div class="image-container">
            <img v-preload :src="mediaItem.poster" alt="Media Item Poster">
        </div>
        <!-- Hover Overlay -->
        <div class="absolute inset-0 p-2 flex flex-col justify-center items-center bg-black bg-opacity-75 opacity-0 hover:opacity-100 transition-opacity">
            <div class="flex flex-col text-left mb-8 h-full">  <!-- Added 'mb-8' for some spacing between the text and buttons -->
                <!-- Display title -->
                <h2 class="text-white text-lg font-semibold mb-2">{{ mediaItem.title }}</h2>
                <!-- Display first 100 characters of the description -->
                <p class="text-white mb-4">{{ mediaItem?.description?.slice(0, 100) }}</p>
            </div>
            <!-- Options or Actions -->
            <div class="space-y-2">
                <button class="border-red-500 text-white bg-opacity-30 border-2 px-3 py-1.5 rounded hover:bg-red-500 hover:bg-opacity-60 hover:text-white transition-all">
                    Add to Library
                </button>
                <button class="border-grey-500 text-white  px-3 py-1.5 rounded hover:bg-blue-500 hover:bg-opacity-60 hover:text-white transition-all">
                    <Cog8ToothIcon class="w-5 h-5 w-[18px] text-white"/>
                </button>
                <!-- Add more options or customize as needed -->
            </div>
        </div>
    </div>
</template>




<script lang="ts">
import { defineComponent, PropType, ref, watch } from 'vue';
import { MediaItem } from "@/models";  // Adjust the path as necessary
import {Cog8ToothIcon} from "@heroicons/vue/24/solid";

const preload = {
  mounted(el) {
    const img = new Image();
    img.src = el.src;
    img.onload = () => {
      el.classList.add('loaded');
    };
  }
};



export default defineComponent({
  name: 'MediaItemPoster',
    components: {
        Cog8ToothIcon
    },
  props: {
    mediaItem: {
      type: Object as PropType<MediaItem>,
      required: true
    }
  },
  directives: {
    preload
  },
  setup(props) {
    const imageLoaded = ref(false);
    const imageError = ref(false);

    watch(() => props.mediaItem.poster, (newValue) => {
      if (newValue) {
        const img = new Image();
        img.onload = () => {
          imageLoaded.value = true;
          imageError.value = false;
        };
        img.onerror = () => {
          imageLoaded.value = false;
          imageError.value = true;
        };
        img.src = newValue;
      } else {
        imageLoaded.value = false;
        imageError.value = true;
      }
    }, { immediate: true });

    return {
      imageLoaded,
      imageError
    };
  },
  computed: {
    randomGradient() {
      // Create an array of possible colors
      const colors = ["#FF5733", "#33FF57", "#5733FF", "#FF3357", "#33FFD1"];
      // Randomly select two colors from the array
      const color1 = colors[Math.floor(Math.random() * colors.length)];
      const color2 = colors[Math.floor(Math.random() * colors.length)];

      return {
        backgroundImage: `linear-gradient(135deg, ${color1}, ${color2})`,
        height: "100%" // You can adjust this based on your needs or make it responsive
      };
    }
  }
});
</script>

<style scoped>
/* Additional styles as necessary */
img {
  opacity: 0;
  transition: opacity 0.3s ease-in-out;
    border-radius: 3px;
}
img.loaded {
  opacity: 1;
}


</style>
