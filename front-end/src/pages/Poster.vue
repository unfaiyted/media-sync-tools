<template>
  <div>
    <router-link to="/">Home</router-link>

    <PosterImage />
  </div>
</template>

<script>
// import PlaylistEditor from "./components/ListEditor.vue";
import PosterImage from "@/components/PosterImage.vue";
// import EndpointTrigger from "@/components/EndpointTrigger.vue";

export default {
  name: "App",
  components: {
    // EndpointTrigger,
    /*PlaylistEditor*/
    PosterImage
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