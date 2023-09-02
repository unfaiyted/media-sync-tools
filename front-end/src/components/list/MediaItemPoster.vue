<template>
  <div class="media-item-poster relative cursor-pointer hover:opacity-80" :style="mediaItem.poster && !imageError ? {} : randomGradient">
    <!-- Conditional Image Poster based on whether it's loaded successfully -->
    <div class="image-container">
      <img v-preload :src="mediaItem.poster" alt="Media Item Poster">
    </div>
    <!-- Hover Overlay -->
    <div class="absolute inset-0 flex flex-col justify-center items-center bg-black bg-opacity-50 opacity-0 hover:opacity-100 transition-opacity">
      <!-- Display title -->
      <h2 class="text-white text-lg font-semibold mb-4">{{ mediaItem.title }}</h2>
      <!-- Options or Actions -->
      <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mb-2">
        Option 1
      </button>
      <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
        Option 2
      </button>
      <!-- Add more options or customize as needed -->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, watch } from 'vue';
import { MediaItem } from "@/models";  // Adjust the path as necessary

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
}
img.loaded {
  opacity: 1;
}


</style>
