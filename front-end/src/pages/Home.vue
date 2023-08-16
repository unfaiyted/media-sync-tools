<template>
  <div>
    <router-link to="/">Home</router-link>
    <router-link to="/poster">Poster</router-link>
    <router-link to="/list">List</router-link>

      Home!!
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
