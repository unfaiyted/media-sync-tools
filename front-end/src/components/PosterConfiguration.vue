<template>
    <div>
        <img :src="posterPath" alt="Poster" />
        <!-- Add your tools for editing the poster here -->
    </div>
</template>

<script>
export default {
    data() {
        return {
            posterPath: this.$route.params.posterPath
        };
    },
    watch: {
        '$route.params.posterPath': function(newPath) {
            this.posterPath = newPath;
        }
    }
}
</script>
