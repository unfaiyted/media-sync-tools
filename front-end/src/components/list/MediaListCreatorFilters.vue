<template>
  <div class="p-4 space-y-4">
    <!-- Dropdown for filters -->
    <div class="relative flex">
      <select v-model="selectedFilter"
              class="block w-fullpx-3 mr-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300">
        <option v-for="filter in availableFilters" :key="filter.name">{{ filter.name }}</option>
      </select>
      <!-- Arrow indicator for dropdown -->
      <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
        <!--        <svg class="w-5 h-5 text-gray-400" viewBox="0 0 20 20" fill="none" stroke="currentColor">-->
        <!--          <path d="M7 7l3-3 3 3m0 6l-3 3-3-3" stroke-width="1.5"></path>-->
        <!--        </svg>-->
      </div>
      <button @click="addFilter"
              class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring focus:ring-blue-200">
        Add Filter
      </button>
    </div>

    <!-- Button to add filter -->

    <!-- Display list of added filters with UI based on datatype -->
    <div v-for="(filter, index) in addedFilters" :key="filter.name" class="space-y-2">
      <label class="block text-lg font-medium">{{ filter.name }}</label>
      <input v-if="filter.type === 'string'" type="text" v-model="filter.value"
             class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300">
      <input v-if="filter.type === 'number'" type="number" v-model="filter.value"
             class="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300">
      <div v-if="filter.type === 'boolean'" class="flex items-center space-x-2">
        <input type="checkbox" v-model="filter.value" class="rounded">
        <span class="text-gray-600">{{ filter.value ? 'True' : 'False' }}</span>
      </div>
      <!-- Add other UI elements for different data types as needed -->
      <button @click="deleteFilter($event, index)"
              class="px-2 py-1 text-red-600 hover:text-red-800 focus:outline-none focus:ring focus:ring-red-200">Delete
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import {defineComponent, ref, watch, reactive} from 'vue';
import {FilterType, mockEmbyFilter, mockFilter} from '@/models/filter';
import {camelCaseToWords} from "@/utils/string";


function getType(value: any): string {
  console.log(value, typeof value)
  if (typeof value === 'boolean') return 'boolean';
  if (typeof value === 'string') return 'string';
  if (typeof value === 'number') return 'number';
  // ... Extend for other data types as needed
  return 'string';
}


export default defineComponent({
  name: 'MediaListCreatorFilters',
  props: {
    filterType: {
      type: String,
      required: true
    }
  },

  setup(props) {
    const selectedFilter = ref('');
    const addedFilters = ref([] as { name: string, type: string, value: any }[]);
    let currentMockFilter = ref(mockFilter[props.filterType as FilterType]);


    watch(() => props.filterType, (newFilterType) => {
      addedFilters.value = [];  // Reset the filters when filterType changes
      console.log(newFilterType,'NEW FILTER TYPE')
      currentMockFilter.value = mockFilter[newFilterType as FilterType];
      console.log(currentMockFilter.value, 'CURRENT MOCK FILTER')
    });


    const deleteFilter = (event: MouseEvent, index: number) => {
      event.preventDefault();
      addedFilters.value.splice(index, 1);
    }

    const addFilter = () => {
      const filterToAdd = availableFilters.value.find(filter => filter.name === selectedFilter.value);
      console.log(filterToAdd)
      if (filterToAdd) {
        addedFilters.value.push({
          name: filterToAdd.name,
          type: filterToAdd.type,
          value: filterToAdd.type === 'boolean' ? false : ''
        });
      }
    }
    const resetFilters = () => {
      addedFilters.value  = [];
      selectedFilter.value = '';
    }
    const updateMockFilter = () => {
      // Using the mockFilter object to get the corresponding mock data
      currentMockFilter.value = mockFilter[props.filterType as keyof typeof mockFilter];
      console.log(currentMockFilter.value, 'CURRENT MOCK FILTER')
    }

    const availableFilters = computed(() => {
      console.log('Updating available filters', currentMockFilter.filterType)
      return Object.keys(currentMockFilter.value)
          .filter(key => key !== 'listId' && key !== 'filterType' && key !== 'clientId' && key !== 'filtersId')
          .map(key => ({
            name: camelCaseToWords(key),
            type: getType(currentMockFilter.value[key])
          }));
    });


    return {
      selectedFilter,
      addedFilters,
      currentMockFilter,
      availableFilters,
      deleteFilter,
      addFilter,
      resetFilters,
      updateMockFilter
    }


  },
});
</script>
