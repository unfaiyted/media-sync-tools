<template>
  <EndpointTrigger />
</template>



<script>
import EndpointTrigger from "@/components/EndpointTrigger.vue";
// import PosterImage from "@/components/PosterImage";

export default {
  name: "App",
  components: {
    // EndpointTrigger,
    /*PlaylistEditor*/
    EndpointTrigger
  },
  methods: {
    savePlaylistData(playlist) {
      // Send the playlist data to the backend API or perform any other action
      console.log(playlist);
      alert("Playlist data saved successfully!");
    },
  },
};
</script>
