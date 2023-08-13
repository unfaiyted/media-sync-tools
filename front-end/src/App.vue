<template>
    <div id="app">
<!--        <PlaylistEditor @save="savePlaylistData" />-->
        <PosterImage />
        <EndpointTrigger />
    </div>
</template>

<script>
// import PlaylistEditor from "./components/PlaylistEditor.vue";
import PosterImage from "./components/PosterImage.vue";
import EndpointTrigger from "@/components/EndpointTrigger.vue";

export default {
    name: "App",
    components: {
        EndpointTrigger,
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
