<template>
  <div class="p-6 bg-gray-100">
    <h1 class="text-2xl font-semibold mb-6">Create a New Media List from Provider</h1>
    <form @submit.prevent="createMediaList">
      <!-- Name -->
      <div class="mb-4">
        <label for="name" class="block mb-2">List Name:</label>
        <input v-model="mediaList.name" type="text" id="name" class="p-2 w-full rounded border" required>
      </div>

      <!-- Poster (assuming it's a URL for simplicity) -->
      <div class="mb-4">
        <label for="poster" class="block mb-2">Poster URL:</label>
        <input v-model="mediaList.poster" type="url" id="poster" class="p-2 w-full rounded border">
      </div>


      <!-- Description -->
      <div class="mb-4">
        <label for="description" class="block mb-2">Description:</label>
        <textarea v-model="mediaList.description" id="description" rows="4"
                  class="p-2 w-full rounded border"></textarea>
      </div>

      <!-- Type -->
      <div class="mb-4">
        <label for="type" class="block mb-2">List Type:</label>
        <select v-model="mediaList.type" id="type" class="p-2 w-full rounded border">
          <option v-for="type in listTypes" :key="type" :value="type">{{ type }}</option>
        </select>
      </div>

      <!-- Sort Name -->
      <div class="mb-4">
        <label for="sortName" class="block mb-2">Sort Name:</label>
        <input v-model="mediaList.sortName" type="text" id="sortName" class="p-2 w-full rounded border">
      </div>

      <!-- Client ID -->
      <div class="mb-4">
<!--        <select v-model="mediaList.clientId" id="clientId" class="p-2 w-full rounded border">-->
<!--          <option v-for="client in clients" :key="client.clientId" :value="client.clientId">{{ client.label }}</option>-->
<!--        </select>-->
        <VSelect :options="clients" label="Provider:" v-model="mediaList.clientId"/>
      </div>
    {{mediaList.clientId}}
      <div class="mb-4">
        <label for="clientId" class="block mb-2">Filters:</label>
        <MediaListCreatorFilters :filterType="filterType"/>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Create List</button>
    </form>
  </div>
</template>


<script lang="ts">
import {ref} from 'vue';
import {MediaList, ListType} from "@/models";
import {useAppConfigStore} from "@/store/appConfigStore";
import MediaListCreatorFilters from "@/components/list/MediaListCreatorFilters.vue";
import VSelect from "@/components/ui/inputs/Select.vue";
import {SelectOption} from "@/models/ui";

export default {
  name: 'MediaListCreator',
  components: {VSelect, MediaListCreatorFilters},
  setup() {
    const store = useAppConfigStore();
    const mediaList = ref<Partial<MediaList>>({
      name: "",
      type: ListType.COLLECTION,
      clientId: '',// Choose a default or make it an empty string
      // Initialize other fields with default values or empty strings
    });

    const filterType = ref('EMBY'); // Default value

    const clients = ref<SelectOption[]>([]);

    onMounted(async () => {
      const clientsData = await store.getClients(); // Replace 'getClients' with your action name if different

      clients.value = clientsData.map(client => ({
        text: client.label,
        value: client.clientId
      } as SelectOption));

      console.log(clientsData)
    });


    const listTypes = Object.values(ListType);  // Assuming ListType is an enum

    const selectedClientName = computed(() => {
      const selectedClient = clients.value.find(client => client.clientId === mediaList.clientId);
      return selectedClient ? selectedClient.label : 'EMBY'; // default to 'EMBY'
    });

    watch(mediaList, (newValue) => {
      console.log('mediaList changed:', newValue);
      const selectedClient = clients.value.find(client => client.value === newValue.clientId);
      console.log('Selected client:', selectedClient);
      filterType.value = selectedClient ? selectedClient.text.toUpperCase() : 'EMBY';
      console.log('filterType:', filterType.value);
      // if we change filter types we should reset the filters
    }, { deep: true });


    const createMediaList = () => {
      // Reset form after submission (optional)
      mediaList.value = {
        name: "",
        type: ListType.COLLECTION,
        // Reset other fields
      };
    };



    return {
      mediaList,
      listTypes,
      clients,
      filterType,
      selectedClientName,
      createMediaList
    };
  }
}
</script>
<style scoped>
/* Any additional styles you'd like for this view */
</style>
