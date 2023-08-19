<template>
  <div>
    <router-link to="/">Home</router-link>


      <MediaPosterTextOptions   />
<!--    <PosterImage />-->
  </div>
</template>

<script lang="ts">
// import PlaylistEditor from "./components/ListEditor.vue";
import PosterImage from "@/components/PosterImage.vue";
import MediaPosterTextOptions from "@/components/poster/MediaPosterTextOptions.vue";
// import EndpointTrigger from "@/components/EndpointTrigger.vue";

export default {
  name: "App",
  components: {
      MediaPosterTextOptions,
    // EndpointTrigger,
    /*PlaylistEditor*/
    PosterImage
  },
  methods: {
  },
};
</script>
