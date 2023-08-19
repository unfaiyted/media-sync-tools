<template>
  <div class="p-6 bg-gray-100 ">
    <!-- Table for Media List Details -->
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-lg font-semibold">{{ mediaLists[0].type }}</h1>

      <!-- Button to trigger popup -->
      <button @click="showOptionsPopup = true" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300">
        +
      </button>
    </div>

    <table class="min-w-full bg-white rounded-lg shadow-md">
      <thead>
      <tr class="text-gray-600 text-left">
        <th class="py-2 px-4">Select</th>
        <th class="py-2 px-4">Name</th>
        <th class="py-2 px-4">Type</th>
        <th class="py-2 px-4">User ID</th>
        <th class="py-2 px-4">Sort Name</th>
        <!-- Add other headers as needed -->
      </tr>
      </thead>
      <tbody>
      <tr v-for="list in mediaLists"
          :key="list.mediaListId"
          class="hover:bg-gray-100 cursor-pointer"
          @click="navigateToList(list.mediaListId)"
          @contextmenu.prevent="handleRightClick($event, list)"
          >
        <td class="py-2 px-4">
          <input type="checkbox">
        </td>
        <td class="py-2 px-4">{{ list.name }}</td>
        <td class="py-2 px-4">{{ list.type }}</td>
        <td class="py-2 px-4">{{ list.clientId }}</td>
        <td class="py-2 px-4">{{ list.sortName }}</td>
        <!-- Add other data fields as needed -->
      </tr>
      </tbody>
    </table>

<!--    <MediaListSyncOptionsPopup
        v-if="showOptionsPopup"
        :media-list-options="selectedListItem"
        @close="showOptionsPopup = false"
    /> -->

    <button @click="openRequestModal">Open Request Modal</button>

    <MediaListOptionsPopup ref="requestModal" />

    <!-- Popup for Media List Options -->
      <!-- Context Menu Popup -->
    <ContextMenu
        :event="contextMenuEvent"
        :items="contextMenuItems"
        ref="contextMenu"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import {syncListToClient} from "@/api/sync";
import {deleteMediaList, fetchMediaListsForUser} from "@/api/lists";
import ContextMenu from "@/components/ui/ContextMenu.vue";
import {MediaListItem} from "@/models";
import { useRouter } from 'vue-router';
import MediaListOptionsPopup from "@/components/list/MediaListOptionsPopup.vue";

export default defineComponent({
  name: 'MediaLists',
  components: {
    ContextMenu,
    MediaListOptionsPopup
  },
  props: {
    mediaLists: {
      type: Array,
      required: true
    },
  },
  setup(props) {
    const showOptionsPopup = ref<boolean>(false);
    const contextMenuEvent = ref<Event | null>(null); // Store the event that triggers the context menu
    const selectedListItem = ref<MediaListItem | null>(null);  // Store the selected list item for context operations
    const requestModal = ref<InstanceType<typeof MediaListOptionsPopup> | null>(null);


    const router = useRouter();

    const navigateToList = (listId: string) => {
      router.push(`/list/${listId}`);
    }

    function handleRightClick(event: Event, item: MediaListItem) {
      if(!item) {
        console.error("List is null");
        return;
      }
      event.preventDefault();
      contextMenuEvent.value = event;
      selectedListItem.value = item; // Store the selected list item for context operations
    }

    const editSelected = () => {
       if(selectedListItem.value)
      router.push(`/list/${selectedListItem.value.mediaListId}/edit`);
    };

    const deleteSelected = async () => {
      if(selectedListItem.value)
      await deleteMediaList(selectedListItem.value.mediaListId);
    };

    const syncSelected = async () => {
      if(selectedListItem.value)
      await syncListToClient('CLIENT_ID', selectedListItem.value.mediaListId);
    };

    const contextMenuItems = [
      {
        label: 'Edit',
        action: editSelected
      },
      {
        label: 'Delete',
        action: deleteSelected
      },
      {
        label: 'Sync',
        action: syncSelected
      }
    ];
    const openRequestModal = () => {
      // requestModal.value.sendSync();
      console.log("Request Modal:", requestModal.value)
      requestModal.value?.openModal();
    }

    return {
      showOptionsPopup,
      navigateToList,
      editSelected,
      contextMenuItems,
      deleteSelected,
      requestModal,
      openRequestModal,
      selectedListItem,
      handleRightClick,
      contextMenuEvent,
      syncSelected,
    };
  }
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  border: 1px solid rgba(0,0,0,0.1);
}
</style>