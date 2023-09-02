<template>
    <div class="bg-gray-100 p-6">
        <div v-if="mediaList">
          <MediaCarousel :media-list="mediaList" :items-to-show="5" />
            <MediaItemsList :media-list="mediaList" :media-list-options="mediaListOptions"/>
        </div>

        <!-- Add a loading spinner or some sort of feedback for when data is loading -->
        <div v-if="loading">
            Loading...
        </div>

        <!-- ... rest of the code ... -->
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onBeforeUnmount } from 'vue';
import {MediaList} from "@/models";
import MediaItemsList from "@/components/list/MediaItemsList.vue";
import { useListStore } from "@/store/listStore";
import MediaCarousel from "@/components/ui/MediaCarousel.vue";

export default defineComponent({
    components: {MediaCarousel, MediaItemsList},
    setup(props, { emit }) {
        // get list id from route params
        const route = useRoute();

        // route.params.listId;

        const mediaListId = ref(route.params.listId);
        const selectedIdType = ref('');
        const searchId = ref('');
        const mediaList = ref<MediaList | null>(null);
        const mediaListOptions = ref({});
        const skipCount = ref(0);
        const limitCount = ref(50);
        const loading = ref(false);
        const noMoreData = ref(false);
        const store = useListStore();

        const loadMoreItems = async (listId: string) => {
            if (loading.value || noMoreData.value) return;
            if(!listId) return;

            loading.value = true;


            const newListItems: MediaList = await store.getListWithItems(
                listId,
                skipCount.value,
                limitCount.value
            );

            console.log('asdfasdfasdfasdfasdf',newListItems);

            if (newListItems.items.length < limitCount.value) {
                noMoreData.value = true;
            }

            if(!mediaList.value) {
                mediaList.value = newListItems;
                loading.value = false;
                return;
            }

            if(!mediaList.value.items) {
                mediaList.value.items = newListItems.items;
                loading.value = false;
                return;
            }
            mediaList.value.items = [...mediaList.value.items, ...newListItems.items];
            loading.value = false;
            skipCount.value += newListItems?.items?.length || 0;
            console.log('skipCount', skipCount?.value);
        };

        const onScroll = () => {
            if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
                console.log('Load more items', route.params.listId);
                loadMoreItems(route.params.listId);
            }
        };

        onMounted(() => {
            // loadMoreItems();
            console.log('Mounted');
            window.addEventListener('scroll', onScroll);
        });

        onBeforeUnmount(() => {
            window.removeEventListener('scroll', onScroll);
        });

        console.log('Load intial', route.params.listId);
        loadMoreItems(route.params.listId);

        return {
            mediaList,
            mediaListOptions,
            loading
        };
    }
});
</script>
