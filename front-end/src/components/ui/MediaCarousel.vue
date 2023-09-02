<template>

  <div class="button-group flex justify-end">
    <button
        v-if="currentIndex !== 0"
        @click="previous"
        class="transition-opacity group-hover:opacity-100 mr-1 mb-1 circle-btn">
      <ChevronLeftIcon class="w-8 h-8 text-black"/>
    </button>

    <button
        v-if="currentIndex + itemsToShow < mediaList.items.length"
        @click="next"
        class="transition-opacity group-hover:opacity-100 circle-btn">
      <ChevronRightIcon class="w-8 h-8 text-black"/>
    </button>
  </div>
  <div ref="carouselContainer" class="flex justify-between items-center carousel-container">



    <transition-group
        name="fade"
        tag="div"
        class="flex space-x-4 overflow-hidden"
        @after-enter="resetHeight"
        @after-leave="resetHeight">
      <div
          v-for="item in visibleItems"
          :key="item.mediaItemId"
          :style="{ width: `calc(${100 / itemsToShow}% - 15px)` }"
          class="flex-none p-4 border border-gray-300 carousel-item">
        <!--
        <img :src="item.item.poster" alt="Media Item Poster" class="w-full h-48 object-cover rounded carousel-image">
        <h2 class="mt-2 font-bold">{{ item.item.title }}</h2>
        <p class="text-gray-600">{{ item.item.year }}</p>
        <p class="text-sm mt-2">{{ item.item.description }}</p>

-->
       <MediaItemPoster :mediaItem="item.item" />

      </div>
    </transition-group>



    <!-- Next Button -->



  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/vue/24/solid';
import MediaItemPoster from "@/components/list/MediaItemPoster.vue";

export default defineComponent({
  name: 'MediaCarousel',
  props: {
    mediaList: {
      type: Object as () => MediaList,
      required: true
    },
    itemsToShow: {
      type: Number,
      default: 5
    }
  },
  components: {
    MediaItemPoster,
    ChevronLeftIcon,
    ChevronRightIcon
  },
  setup(props) {
    console.log('carousel',props)
    const carouselContainer = ref(null);
    const isLoadingItems = ref(false);
    const currentIndex = ref(0);
    console.log('carousel',props?.mediaList?.items?.length, props?.itemsToShow, currentIndex?.value)

    const visibleItems = computed(() => {
      return props.mediaList.items.slice(currentIndex.value, currentIndex.value + props.itemsToShow);
    });

    const next = () => {
      if (currentIndex.value + props.itemsToShow < props.mediaList.items.length) {
        currentIndex.value += props.itemsToShow;

        const currentHeight = carouselContainer.value.clientHeight;
        carouselContainer.value.style.minHeight = `${currentHeight}px`;
        carouselContainer.value.style.maxHeight = `${currentHeight}px`;
      }
    };

    const previous = () => {
      if (currentIndex.value > 0) {
        currentIndex.value -= props.itemsToShow;
        const currentHeight = carouselContainer.value.clientHeight;
        carouselContainer.value.style.minHeight = `${currentHeight}px`;
        carouselContainer.value.style.maxHeight = `${currentHeight}px`;

      }
    };

    const resetHeight = () => {
      carouselContainer.value.style.minHeight = '';
      carouselContainer.value.style.maxHeight = '';
    };

    return {
      currentIndex,
      carouselContainer,
      isLoadingItems,
      visibleItems,
      resetHeight,

      next,
      previous
    };
  }
});
</script>

<style scoped>
/* These styles will provide a slide + fade effect when items change */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter, .slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}

/* These styles will provide a slide + fade effect when items change */
.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter, .slide-fade-leave-to {
  transform: translateX(10px);
  opacity: 0;
}

/* Hide the buttons initially and show them on hover */
.group:hover .opacity-0 {
  opacity: 100;
}

.carousel-container {
  width: 100%;
  overflow: hidden;
  position: relative;
 }

.carousel-item {
  min-width: 0;
  max-width: 100%;
  flex: 0 0 auto;
  transition: transform 0.3s ease;
}
.circle-btn {
  background-color: transparent;
  border: 2px solid black; /* Change color to black */
  border-radius: 50%;
  padding: 2px;  /* Reduce padding for smaller size */
  width: 24px;  /* Specify width and height for consistent size */
  height: 24px;
  display: flex;  /* Center the icon in the button */
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.circle-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);  /* 10% black background on hover */
}


</style>
