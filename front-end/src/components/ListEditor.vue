<template>
    <div class="p-4">
        <h2>Create a New List</h2>
        <form @submit.prevent="savePlaylist">
            <div>
                <label for="name">Name:</label>
                <input type="text" v-model="list.name" required />
            </div>
            <div>
                <label for="sortName">Sort Name:</label>
                <input type="text" v-model="list.sort_name" required />
            </div>
            <div>
                <label for="provider">Provider:</label>
                <select v-model="list.provider" required>
                    <option value="self">Self</option>
                    <option value="trakt">Trakt</option>
                    <!-- Add more options for other providers -->
                </select>
            </div>
            <div>
                <label>Filters:</label>
                <div v-for="(filter, index) in list.filters" :key="index">
                    <select v-model="filter.type" @change="resetFilterValue(filter)" required>
                        <option value="genre">Genre</option>
                        <option value="is_watched">Is Watched</option>
                        <option value="name">Name</option>
                        <option value="ai_rule">AI Rule</option>
                        <!-- Add more options for other filter types -->
                    </select>
                    <input v-if="filter.type !== 'ai_rule'" type="text" v-model="filter.value" required />
                    <textarea v-else v-model="filter.value" rows="3" required></textarea>
                    <button type="button" @click="removeFilter(index)">Remove</button>
                </div>
                <button type="button" @click="addNewFilter">Add Filter</button>
            </div>
            <div>
                <label>Media Types:</label>
                <div v-for="(mediaType, index) in list.media_types" :key="index">
                    <input
                        type="text"
                        :value="mediaType"
                        @input="updateMediaType(index, $event.target.value)"
                        required
                    />
                    <button type="button" @click="removeMediaType(index)">Remove</button>
                </div>
                <button type="button" @click="addNewMediaType">Add Media Type</button>
            </div>
            <div>
                <label for="addPrevWatched">Add Previously Watched:</label>
                <input type="checkbox" v-model="list.options.add_prev_watched" />
            </div>
            <div>
                <label for="limit">Limit:</label>
                <input type="number" v-model="list.options.limit" required />
            </div>
            <div>
                <label for="sort">Sort:</label>
                <input type="text" v-model="list.options.sort" required />
            </div>
            <div>
                <label for="sortOrder">Sort Order:</label>
                <input type="text" v-model="list.options.sort_order" required />
            </div>

            <button type="submit">Save Playlist</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            list: {
                name: "",
                sort_name: "",
                provider: "self",
                filters: [],
                media_types: [],
                options: {
                    add_prev_watched: true,
                    limit: 1500,
                    sort: "recently_watched",
                    sort_order: "desc",
                },
            },
        };
    },
    methods: {
        savePlaylist() {
            // Emit an event to notify the parent component to save the playlist data
            this.$emit("save", this.list);
        },
        addNewFilter() {
            this.list.filters.push({ type: "genre", value: "" });
        },
        removeFilter(index) {
            this.list.filters.splice(index, 1);
        },
        resetFilterValue(filter) {
            filter.value = "";
        },
        updateMediaType(index, value) {
            this.list.media_types[index] = value;
        },
        addNewMediaType() {
            this.list.media_types.push("");
        },
        removeMediaType(index) {
            this.list.media_types.splice(index, 1);
        },
    },
};
</script>
