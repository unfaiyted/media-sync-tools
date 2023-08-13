
<template>
  <div id="app" class="bg-gray-200 min-h-screen">
    <Header />
    <div class="flex">
      <Sidebar />
      <router-view class="flex-grow bg-gray-100" />
    </div>
  </div>
</template>

<script>
import Sidebar from "./components/ui/SidebarView"
import Header from "./components/ui/HeaderView"
// import PlaylistEditor from "./components/ListEditor.vue";
// import PosterImage from "./components/PosterImage.vue";
// import EndpointTrigger from "@/components/EndpointTrigger.vue";

export default {
    name: "App",
    components: {
      // EndpointTrigger,
      Sidebar,
      Header
      /*PlaylistEditor*/
      // PosterImage
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
