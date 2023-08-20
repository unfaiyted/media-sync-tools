<template>
  <div>
<!--    <router-link to="/">Home</router-link>-->

      <MediaPosterTextOptions :value="poster.text"   />
    <MediaPosterGradientOptions :gradient-options="poster.gradient" />
    <MediaPosterBackgroundOptions :background-options="poster.background" />

    <div v-if="poster.border">
      Poster Border
      <MediaPosterBorderOptions :value="poster.border"/>
    </div>


    <MediaPosterIconOptions :icon-options="poster.icon" />
    <MediaPosterOverlayOptions :overlay-options="poster.overlays" />

<!--    <PosterImage />-->
  </div>
</template>

<script lang="ts">
// import PlaylistEditor from "./components/ListEditor.vue";
import PosterImage from "@/components/PosterImage.vue";
import MediaPosterTextOptions from "@/components/poster/MediaPosterTextOptions.vue";
import {IconPosition, MediaImageType, MediaPoster} from "@/models";
import MediaPosterGradientOptions from "@/components/poster/MediaPosterGradientOptions.vue";
import MediaPosterBackgroundOptions from "@/components/poster/MediaPosterBackgroundOptions.vue";
import MediaPosterIconOptions from "@/components/poster/MediaPosterIconOptions.vue";
import MediaPosterBorderOptions from "@/components/poster/MediaPosterBorderOptions.vue";
import MediaPosterOverlayOptions from "@/components/poster/MediaPosterOverlays.vue";
// import EndpointTrigger from "@/components/EndpointTrigger.vue";



export default defineComponent({
  name: "App",
  components: {
    MediaPosterBackgroundOptions,
    MediaPosterGradientOptions,
      MediaPosterTextOptions,
      MediaPosterIconOptions,
      MediaPosterOverlayOptions,
    MediaPosterBorderOptions,

    // EndpointTrigger,
    /*PlaylistEditor*/
    PosterImage
  },
  methods: {
  },
  setup(props) {
    const poster = ref<MediaPoster>({
      mediaPosterID: crypto.randomUUID(),
      text: {
        enabled: true,
        text: 'Hello World!',
        // font: 'Arial',
        // size: 24,
        // style: 'normal',
        // weight: 'normal',
        // align: 'left',
        position: [0, 0],
        color: [255, 255, 255],
        shadow: {
          enabled: true,
          color: [0, 0, 0],
          blur: 0,
          offset: 0,
          transparency: 100,
        },
        border: {
          enabled: true,
          color: [0, 0, 0],
          width: 1,
          height: 1,
        },
      },
      width: 400,
      height: 600,
      type: MediaImageType.POSTER,
      gradient: {
         enabled: true,
          colors: [
            [255, 255, 255],
            [0, 0, 0],
          ],
          opacity: 0.5,
          type: 'linear',
          angle: 0
      },
      background: {
        url: '',
        enabled: true,
        opacity: 1.0,
        color: [0, 0, 0],
        border: {
          enabled: true,
          color: [0, 0, 0],
          width: 1,
          height: 1,
        },

      },
      border: {
        enabled: true,
        color: [0, 0, 0],
        width: 1,
        height: 1,
      },
      icon: {
        enabled: true,
        path: '',
        position: IconPosition.MIDDLE,
        size: [200, 250],

      },
      overlays: [{
        enabled: true,
        cornerRadius: 0,
        transparency: 0,
        icon: {
          enabled: true,
          path: '',
          size: [0, 0],
          position: IconPosition.LEFT,
        },
        position: IconPosition.LEFT // Default position, adjust if needed
      }]
    });

    return {
      poster
    }
  }
});
</script>
