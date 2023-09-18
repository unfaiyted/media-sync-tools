<template>
  <div>

  </div>
</template>

<script lang="ts">

export default {
  name: "App",
  components: {
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
