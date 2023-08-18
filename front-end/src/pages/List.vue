<template>
  <div class="bg-gray-100 p-6">

    <MediaItemsList :media-list="mediaList" :media-list-options="mediaListOptions"/>

    <!-- ... rest of the code ... -->
  </div>
</template>

<script lang="ts">
import MediaItemsList from "@/components/list/MediaItemsList.vue";
import MediaLists from "@/components/list/MediaLists.vue";
import {fetchMediaList, fetchMediaListsForUser, fetchMediaListWithItems} from "@/api/lists";
export default defineComponent({
  components: {MediaLists, MediaItemsList},
  props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      mediaListId: this.$route.params.listId,
      selectedIdType: '',
      searchId: '',
      mediaList: {
        mediaListId: "ml12345",
        name: "Favorite Movies",
        type: "MOVIES", // assuming ListType has a value "MOVIES"
        sortName: "Favorites",
        clientId: "cl12345",
        filters: [
          {
            // Add the structure of the Filter here
            filterId: "f12345",
            filterType: "Genre",
            filterValue: "Action"
          }
        ],
        items: [
          {
            itemId: "i12345",
            listId: "l12345",
            name: "Inception",
            poster: "path_to_inception_poster.jpg",
            description: "A movie about dreams within dreams.",
            year: "2010",
            sourceId: "s12345",
            releaseDate: "2010-07-16",
            dateAdded: "2021-08-17",
            imdbId: "tt1375666",
            tvdbId: "tv12345",
            tmdbId: "tm12345",
            traktId: "tr12345",
            aniList: "a12345",
            type: "MOVIE" // assuming MediaType has a value "MOVIE"
          },
          {
            itemId: "i12345",
            listId: "l12345",
            name: "Inception",
            poster: "path_to_inception_poster.jpg",
            description: "A movie about dreams within dreams.",
            year: "2010",
            sourceId: "s12345",
            releaseDate: "2010-07-16",
            dateAdded: "2021-08-17",
            imdbId: "tt1375666",
            tvdbId: "tv12345",
            tmdbId: "tm12345",
            traktId: "tr12345",
            aniList: "a12345",
            type: "MOVIE" // assuming MediaType has a value "MOVIE"
          },
          {
            itemId: "i12345",
            listId: "l12345",
            name: "Inception",
            poster: "path_to_inception_poster.jpg",
            description: "A movie about dreams within dreams.",
            year: "2010",
            sourceId: "s12345",
            releaseDate: "2010-07-16",
            dateAdded: "2021-08-17",
            imdbId: "tt1375666",
            tvdbId: "tv12345",
            tmdbId: "tm12345",
            traktId: "tr12345",
            aniList: "a12345",
            type: "MOVIE" // assuming MediaType has a value "MOVIE"
          },
          // ... add more items as required
        ],
        userId: "u12345",
        user: {
          userId: "u12345",
          username: "john_doe",
          email: "john.doe@example.com"
          // ... add more user fields as required
        },
        options: {
          mediaListOptionsId: "mlo12345",
          sync: true,
          updateImages: false,
          configClientId: "cc12345",
          includeLibraries: [
            {
              // Add the structure of the Library here
              libraryId: "lib12345",
              libraryName: "Default Library"
            }
          ],
          deleteExisting: false,
          deleteWatchlist: true
        }
      },
      mediaListOptions: {
        mediaListId: "ml12345",
        type: "MOVIES", // assuming ListType has a value "MOVIES"
        configId: "c12345",
        sync: true,
        updateImages: true,
        configClientId: "cc12345",
        includeLibraries: [
          {
            libraryId: "lib12345",
            libraryName: "Default Library"
          }
        ],
        deleteExisting: false,
        deleteWatchlist: true
      }



    };
  },
  watch: {
    // Watch for changes to the items prop and update localItems when it changes
    // items(newItems) {
    //   this.localItems = [...newItems];
    // }
  },
  async mounted() {
    this.mediaList = await fetchMediaListWithItems(this.mediaListId);
  },
  methods: {
    getMediaLists: async function() {
      // Handle logic to get the MediaLists
      console.log("MediaList:", this.mediaList);
      this.mediaList = await fetchMediaListWithItems(this.mediaListId);
    },
  }});
</script>
