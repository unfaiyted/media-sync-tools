<template>
    <Modal :is-open="isOpen" @cancel-action="closeModal" @do-action="doAction">
        <h2 class="text-white text-xl font-bold mb-4">Add Movie </h2>
        <p class="text-white text-lg mb-2">{{ mediaListItem?.item.title }}</p>
<!--        <p class="text-indigo-300 mb-4">This request will be approved.</p>-->


        <img :src="mediaListItem.item?.poster" :alt="mediaListItem.item?.tagline" class="max-w-[100px] h-auto mb-2">
        <div class="mb-4">
            <label class="block text-white text-sm font-bold mb-2" for="tags">Add to Clients(s):</label>
            <ClientButtonGroup :type="ClientType.UTILITY" :is-config="true" @selectedClientsChanged="handleSelectedClients"/>
        </div>


        <!-- Flex container for 3 sections -->
        <div class="flex justify-between mb-4 space-x-2">
            <div class="flex-1">
                <label class="block text-white text-sm font-bold mb-2" for="folder">File Storage Location</label>
                <VSelect :options="configLibraries" v-model="mediaItemOptions.syncLibraryId"/>
            </div>

        </div>

        <div class="mb-4 space-y-2">
            <label class="block text-white text-sm font-bold">Options:</label>
            <div>
                <VCheckbox v-model="mediaItemOptions.updateImages" label="Update client poster images"/>
            </div>
            <div>
                <VCheckbox v-model="mediaItemOptions.deleteExisting" label="Something"/>
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
import {defineComponent, onBeforeMount, ref} from 'vue';
import {ClientType, ConfigClient, MediaItemOptions, MediaItemType, MediaListItem, MediaListType} from "@/models";
import ClientButtonGroup from "@/components/ui/ClientButtonGroup.vue";
import Modal from "@/components/ui/Modal.vue";
import VSelect from "@/components/ui/inputs/Select.vue";
import {SelectOption} from "@/models/ui";
import {useAppConfigStore} from "@/store/appConfigStore";
import VCheckbox from "@/components/ui/inputs/Checkbox.vue";
import {useListStore} from "@/store/listStore";

export default defineComponent({
    name: 'MediaItemOptionsPopup',
    components: {VCheckbox, VSelect, ClientButtonGroup, Modal},
    props: {
        selectedItem: Object as () => MediaListItem,
    },
    setup(props, {emit}) {
        // const store = useAppConfigStore();
        const store = useAppConfigStore();
        const configLibraries = ref<SelectOption[]>([]);
        const isOpen = ref(false);
        const mediaListItem = ref<MediaListItem>();
        const selectedClients = ref<ConfigClient[]>([]);
        const mediaItemTypes: SelectOption[] = Object.values(MediaItemType).map((type) => {
            return {
                value: type,
                text: type,
            };
        })
        const mediaItemOptions = ref<MediaItemOptions>({
                mediaItemOptionsId: crypto.randomUUID(),
                userId: '',
                mediaItemId: '',
                acquireClient: undefined,
                type: MediaItemType.EPISODE,
                updateImages: false,
            })
        ;

        onBeforeMount(async () => {
            const store = useAppConfigStore();
            configLibraries.value = (await store.getLibraries()).map((library) => {
                return {
                    value: library.libraryId as string,
                    text: library.name,
                };
            })

        });


        const doAction = () => {
            // Implement the sync logic here
            console.log(mediaItemOptions.value)
            const listStore = useListStore();
            listStore.syncListToProviders(mediaItemOptions.value);
            console.log("Request Sent!");
            isOpen.value = false;
        };

        const openModal = async (item) => {
            const store = useAppConfigStore();
            console.log('open modal', selectedClients)
            mediaItemOptions.value.mediaListId = props.selectedItem?.mediaListId as string;
            mediaListItem.value = props.selectedItem;
            isOpen.value = true;
        };

        const closeModal = () => {
            isOpen.value = false;
            emit('close-modal');
        };


        const handleSelectedClients = (selectedClients: ConfigClient[]) => {
            console.log('selected xxxx clients changed', selectedClients)
            mediaItemOptions.value.clients = selectedClients;
        }

        return {
            isOpen,
            openModal,
            ClientType,
            mediaListItem,
            handleSelectedClients,
            selectedClients,
            configLibraries,
            mediaItemTypes,
            mediaItemOptions,
            doAction,
            closeModal
        };
    }
});
</script>

<style scoped>
/* Optional additional styling */
</style>
