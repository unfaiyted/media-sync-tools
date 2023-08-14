<template>
    <table>
        <thead>
        <tr>
            <th>Title</th>
            <th>Year</th>
            <th>Description</th>
            <th>Poster</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="movie in movies" :key="movie.title">
            <td>{{ movie.title }}</td>
            <td>{{ movie.year }}</td>
            <td>{{ movie.description }}</td>
            <td>
                <img :src="movie.poster" alt="Movie Poster" @click="editPoster(movie)" />
            </td>
        </tr>
        </tbody>
    </table>
</template>

<script>
export default {
    data() {
        return {
            movies: []
        };
    },
    methods: {
        fetchMovies() {
            fetch('/movies')
                .then(response => response.json())
                .then(data => {
                    this.movies = data;
                });
        },
        editPoster(movie) {
            // Assuming you have another Vue component or view to handle poster configuration/editing
            this.$router.push({
                name: 'PosterConfiguration',
                params: { posterPath: movie.poster }
            });
        }
    },
    created() {
        this.fetchMovies();
    }
}
</script>
