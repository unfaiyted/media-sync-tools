<template>
  <div class="flex">
        <MediaPosterSidebar :poster="poster" />
        <div class="flex-grow">
          <div class="flex justify-end bg-gray-300 mb-4">
            <VButton
                class="text-white m-2"
                label="Actions"
                @click="fetchImage"
                />
            <VButton @click="fetchImage" class="search-button m-2">Link to...</VButton>
          </div>

            <PosterImage :poster="poster" />
            </div>
  </div>
</template>

<script lang="ts">
import PosterImage from "@/components/poster/PosterImage.vue";
import MediaPosterTextOptions from "@/components/poster/MediaPosterTextOptions.vue";
import MediaPosterGradientOptions from "@/components/poster/MediaPosterGradientOptions.vue";
import MediaPosterBackgroundOptions from "@/components/poster/MediaPosterBackgroundOptions.vue";
import MediaPosterIconOptions from "@/components/poster/MediaPosterIconOptions.vue";
import MediaPosterBorderOptions from "@/components/poster/MediaPosterBorderOptions.vue";
import MediaPosterOverlayOptions from "@/components/poster/MediaPosterOverlays.vue";
import MediaPosterSidebar from "@/components/poster/MediaPosterSidebar.vue";
import {usePosterStore} from "@/store/posterStore";
import { MediaPoster} from "@/models";
import VButton from "@/components/ui/inputs/Button.vue";


export default defineComponent({
  name: "App",
  components: {
    VButton,
    MediaPosterSidebar,
    MediaPosterBackgroundOptions,
    MediaPosterGradientOptions,
    MediaPosterTextOptions,
    MediaPosterIconOptions,
    MediaPosterOverlayOptions,
    MediaPosterBorderOptions,
    PosterImage
  },
  methods: {
  },
  setup(props) {
    const store = usePosterStore();

    const poster = ref<MediaPoster>(store.setDefaultPoster());

    const fetchImage = () => {
      console.log('fetching image', poster.value)
      store.createPoster(poster.value);
      console.log(poster.value)

    };

    return {
      poster,
      fetchImage
    }
  }
});
</script>

<style>
.search-button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #0056b3;
}

</style>
