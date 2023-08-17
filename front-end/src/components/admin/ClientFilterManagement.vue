<template>
    <div class="p-6">
        <!-- Create Filter Type Field -->
        <h2 class="text-lg font-semibold mb-4">Create Filter Type</h2>
        <div class="mb-4">
            <input v-model="newFilterType.label" class="input" placeholder="Label">
        </div>
        <div class="mb-4">
            <input v-model="newFilterType.name" class="input" placeholder="Name">
        </div>
        <div class="mb-4">
            <select v-model="newFilterType.type" class="input">
                <option value="text">Text</option>
                <option value="number">Number</option>
                <option value="boolean">Boolean</option>
            </select>
        </div>
        <button @click="createFilterType" class="btn btn-primary">Add Filter Type</button>

        <!-- List Filter Types -->
        <h2 class="text-lg font-semibold mt-8 mb-4">Filter Types</h2>
        <ul v-if="filterTypes.length">
            <li v-for="filterType in filterTypes" :key="filterType.filterTypeId" class="mb-2">
                {{ filterType.label }} ({{ filterType.name }}, {{ filterType.type }})
                <button @click="openEditModal(filterType)" class="btn btn-secondary">Edit</button>
                <button @click="deleteFilterType(filterType.filterTypeId)" class="btn btn-danger">Delete</button>
            </li>
        </ul>

        <!-- Update Filter Type Modal -->
        <transition name="modal" enter-active-class="transition-opacity ease-out duration-300" leave-active-class="transition-opacity ease-in duration-300">
            <div v-if="showEditModal" class="fixed inset-0 flex items-center justify-center">
                <div class="modal-overlay absolute inset-0 bg-gray-900 opacity-75" @click="closeEditModal"></div>
                <div class="modal-container bg-white w-1/2 mx-auto p-6 rounded shadow-lg">
                    <h3 class="text-lg font-semibold mb-4">Edit Filter Type</h3>
                    <div class="mb-4">
                        <input v-model="editingFilterType.label" class="input" placeholder="Label">
                    </div>
                    <div class="mb-4">
                        <input v-model="editingFilterType.name" class="input" placeholder="Name">
                    </div>
                    <div class="mb-4">
                        <select v-model="editingFilterType.type" class="input">
                            <option value="text">Text</option>
                            <option value="number">Number</option>
                            <option value="boolean">Boolean</option>
                        </select>
                    </div>
                    <div class="flex justify-end">
                        <button @click="updateFilterType" class="btn btn-primary">Update</button>
                        <button @click="closeEditModal" class="btn btn-secondary ml-2">Cancel</button>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { createFilterType, deleteFilterType, fetchFilterTypes, updateFilterType } from '@/api/clients';
import {Client as MediaClient, FilterTypes} from '@/models';

export default defineComponent({
    props: {
        client: {
            type: Object as () => MediaClient,
            required: true
        } // Define the prop for the client object
    },
    setup(props) {
        const newFilterType = ref({
            label: '',
            name: '',
            type: 'text' // Default value
        } as FilterTypes);
        const filterTypes = ref([] as FilterTypes[]);
        const editingFilterType = ref({} as FilterTypes);
        const showEditModal = ref(false);

        const fetchFilterTypesList = async () => {
            filterTypes.value = await fetchFilterTypes(props.client.clientId);
        };

        const createFilterType = async () => {
            await createFilterType({ ...newFilterType.value, clientId: props.client.clientId });
            fetchFilterTypesList();
        };

        const updateFilterType = async () => {
            const updatedFilterType = await updateFilterType(editingFilterType.value);
            const index = filterTypes.value.findIndex(ft => ft.filterTypeId === editingFilterType.value.filterTypeId);
            if (index !== -1) {
                filterTypes.value[index] = updatedFilterType;
            }
            closeEditModal();
        };

        const deleteFilterType = async (filterTypeId: string) => {
            await deleteFilterType(filterTypeId);
            filterTypes.value = filterTypes.value.filter(ft => ft.filterTypeId !== filterTypeId);
        };

        const openEditModal = (filterType: FilterTypes) => {
            editingFilterType.value = { ...filterType };
            showEditModal.value = true;
        };

        const closeEditModal = () => {
            editingFilterType.value = {} as FilterTypes;
            showEditModal.value = false;
        };

        // Fetch filter types on component mount
        fetchFilterTypesList();

        return {
            newFilterType,
            filterTypes,
            editingFilterType,
            showEditModal,
            createFilterType,
            updateFilterType,
            deleteFilterType,
            openEditModal,
            closeEditModal
        };
    }
});
</script>

<style scoped>
/* Add your Tailwind CSS classes and custom styles here */
</style>
