<template>
    <Modal :is-open="isOpen" @cancel-action="closeModal" @do-action="doAction">
        <h2 class="text-white text-xl font-bold mb-4">Add Movie (Radarr/Sonarr)</h2>
        <p class="text-white mb-2">{{ mediaListItem?.name}}</p>
        <p class="text-indigo-300 mb-4">This request will be approved.</p>

        <div class="mb-4">
            <label class="block text-white text-sm font-bold mb-2" for="tags">Add to Clients(s):</label>
            <ClientButtonGroup :type="ClientType.UTILITY" :is-config="true" @selectedClientsChanged="handleSelectedClients" />
        </div>


        <!-- Flex container for 3 sections -->
        <div class="flex justify-between mb-4 space-x-2">
            <div class="flex-1">
                <label class="block text-white text-sm font-bold mb-2" for="folder">File Storage Location</label>
                <VSelect :options="configLibraries" v-model="mediaListOptions.syncLibraryId" />
            </div>

        </div>

        <div class="mb-4 space-y-2">
            <label class="block text-white text-sm font-bold">Options:</label>
            <div>
                <VCheckbox v-model="mediaItemOptions.updateImages" label="Update client poster images"/>
            </div>
            <div>
                <VCheckbox v-model="mediaItemOptions.deleteExisting" label="" />
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
import {MediaListItem, ClientType, MediaListOptions, MediaListType, ConfigClient} from "@/models";
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
        const configLibraries = ref<SelectOption[]>([]);
        const isOpen = ref(false);
        const mediaListItem = ref<MediaListItem>();
        const selectedClients =  ref<ConfigClient[]>([]);
        const mediaListTypes: SelectOption[] = Object.values(MediaListType).map((type) => {
            return {
                value: type,
                text: type,
            };
        }).filter((type) => type.value !== MediaListType.LIBRARY)
        const mediaItemOptions = ref<MediaItemOptions>({
            mediaListOptionsId: crypto.randomUUID(),
            userId: '',
            mediaListId: '',
            syncLibraryId: '',
            clients: [],
            type: MediaListType.COLLECTION,
            sync: true,
            updateImages: false,
            deleteExisting: false,
        });

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
            console.log(mediaListOptions.value)
            const listStore = useListStore();
            listStore.syncListToProviders(mediaListOptions.value);
            console.log("Request Sent!");
            isOpen.value = false;
        };

        const openModal = async (item) => {
            const store = useAppConfigStore();
            console.log('open modal', selectedClients)
            mediaListOptions.value.mediaListId = props.selectedItem?.mediaListId as string;
            mediaListItem.value = props.selectedItem;
            isOpen.value = true;
        };

        const closeModal = () => {
            isOpen.value = false;
            emit('close-modal');
        };


        const handleSelectedClients = (selectedClients: ConfigClient[]) => {
            console.log('selected xxxx clients changed', selectedClients)
            mediaListOptions.value.clients = selectedClients;
        }

        return {
            isOpen,
            openModal,
            ClientType,
            mediaListItem,
            handleSelectedClients,
            selectedClients,
            configLibraries,
            mediaListTypes,
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
