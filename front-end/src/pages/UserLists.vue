<template>
  <div class="bg-gray-100 p-6">

    <MediaLists :media-lists="mediaLists"/>

    <!-- ... rest of the code ... -->
  </div>
</template>

<script lang="ts">
import MediaListView from "@/components/list/MediaItemsList.vue";
import {MediaListOptions, MediaList, ListType} from "@/models";
import MediaLists from "@/components/list/MediaLists.vue";
import {fetchMediaList, fetchMediaListsForUser} from "@/api/lists";
export default defineComponent({
    components: {MediaLists, MediaListView},
    props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
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
        mediaLists: [
          {
           mediaListId: '1a2b3c4d',
           name: 'Top 10 Movies of 2020',
           type: ListType.COLLECTION,
           sortName: 'Top Movies 2020',
           clientId: 'client1234',
           userId: 'user5678'
           },
           {
           mediaListId: '2b3c4d5e',
           name: 'Binge-worthy TV Shows',
           type: ListType.PLAYLIST,
           sortName: 'Binge TV Shows',
           clientId: 'client5678',
           userId: 'user1234'
         }
       ] as MediaList[],
        mediaListOptions:{
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
    this.mediaLists = await fetchMediaListsForUser("APPUSERID");
  },
  methods: {
    getMediaLists: async function () {
      // Handle logic to get the MediaLists
      console.log("MediaLists:", this.mediaLists);
      this.mediaLists = await fetchMediaList("0988d3bf-3766-474b-90f2-eb1b7ffff4c7");
    }
  }
});
</script>
