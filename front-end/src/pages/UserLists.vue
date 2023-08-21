<template>
  <div class="bg-gray-100 p-6">

    <div v-if="mediaLists">
      <MediaLists :media-lists="mediaLists"/>
    </div>

    <!-- ... rest of the code ... -->
  </div>
</template>

<script lang="ts">
import MediaLists from "@/components/list/MediaLists.vue";
import {useListStore} from "@/store/listStore";

export default defineComponent({
  components: {MediaLists},
  props: {
    items: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      mediaLists: null,
    };
  },
  async mounted() {
    const store = useListStore();
    this.mediaLists = await store.fetchAllLists();
    console.log("MediaLists:", this.mediaLists)
  },
  methods: {
  }});
</script>
