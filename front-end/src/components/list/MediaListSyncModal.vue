<template>
    <Modal :is-open="isOpen" :cancel-action="closeModal" :do-action="doAction">
        <h2 class="text-white text-xl font-bold mb-4">Sync List</h2>
        <p class="text-white mb-2">{{ mediaListItem?.name}}</p>
<!--        <p class="text-indigo-300 mb-4">This request will be approved.</p>-->

        <!-- Flex container for 3 sections -->
        <div class="flex justify-between mb-4 space-x-2">

            <div class="flex-1">
                <label class="block text-white text-sm font-bold mb-2" for="quality">List Type</label>
                <VSelect options="" />
            </div>

            <div class="flex-1">
                <label class="block text-white text-sm font-bold mb-2" for="folder">Libraries</label>
                <VSelect :options="['Movies', 'TV Shows']" />
            </div>

            <div class="flex-1">
                <label class="block text-white text-sm font-bold mb-2" for="tags">Clients</label>
                <VSelect :options="['Plex', 'Jellyfin', 'Emby']" />
            </div>

        </div>

        <div class="mb-4">
            <label class="block text-white text-sm font-bold mb-2" for="tags">Sync to</label>

        </div>


        <div class="mb-4 space-y-2">
            <label class="block text-white text-sm font-bold">Options:</label>

            <div>
                <input type="checkbox" id="updateImages" v-model="mediaListOptions.updateImages">
                <label for="updateImages" class="text-white ml-2">Update client poster images</label>
            </div>
            <div>
                <input type="checkbox" id="deleteExisting" v-model="mediaListOptions.deleteExisting">
                <label for="deleteExisting" class="text-white ml-2">Delete list if one with same name exists.</label>
            </div>

        </div>

        <div class="flex items-center mb-4">
            <img src="https://plex.tv/users/8366c34ded926e94/avatar?c=1685649373" alt="User Avatar" class="h-8 w-8 rounded-full mr-4">
            <div>
                <p class="text-white">Faiyt</p>
                <p class="text-sm text-gray-400">unfaiyted@gmail.com</p>
            </div>
        </div>


    </Modal>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import {MediaListItem, ClientType, MediaListOptions} from "@/models";
import ClientButtonGroup from "@/components/ui/ClientButtonGroup.vue";
import Modal from "@/components/ui/Modal.vue";
import VSelect from "@/components/ui/inputs/Select.vue";

export default defineComponent({
    name: 'MediaListSyncModal',
    components: {VSelect, ClientButtonGroup, Modal},
    setup() {
        const isOpen = ref(false);
        const mediaListItem = ref<MediaListItem>();
        const mediaListOptions = ref<MediaListOptions>({
            mediaListOptionsId: '',
            mediaListId: '',
            syncLibraryId: '',
            sync: false,
            updateImages: false,
            deleteExisting: false,
        });

        const doAction = () => {
            // Implement the sync logic here
            console.log("Request Sent!");
            isOpen.value = false;
        };

        const openModal = (item: MediaListItem) => {
            mediaListItem.value = item;
            isOpen.value = true;
        };

        const closeModal = () => {
            isOpen.value = false;
        };

        return {
            isOpen,
            openModal,
            ClientType,
            mediaListItem,
            mediaListOptions,
            doAction,
            closeModal
        };
    }
});
</script>

<style scoped>
/* Optional additional styling */
</style>
