<template>
  <div class="bg-gray-100 p-6">

      <div v-if="mediaList">
        <MediaItemsList :media-list="mediaList" :media-list-options="mediaListOptions"/>
      </div>

    <!-- ... rest of the code ... -->
  </div>
</template>

<script lang="ts">
import MediaItemsList from "@/components/list/MediaItemsList.vue";
import MediaLists from "@/components/list/MediaLists.vue";
import {useListStore} from "@/store/listStore";


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
      mediaList: null,
        mediaListOptions:{}
    };
  },
  async mounted() {
      const store = useListStore();

      this.mediaList = await store.getListWithItems(this.mediaListId);
      console.log("MediaList:", this.mediaList)
  },
  methods: {
  }});
</script>
