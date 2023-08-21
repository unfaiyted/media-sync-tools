<template>
  <div v-if="editingFields">
    <div v-for="field in clientFields" :key="field.name" class="mb-4 flex">
      <label :for="field.name" class="block text-white mb-2 mr-3 w-[40%]">{{ toReadableString(field.name) }}:</label>
      <input v-model="editingFields[field.name]"
             @input="handleInputChange(field)"
             :id="field.name"
             class="block appearance-none w-full bg-gray-700 border border-gray-600 text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500"
             :placeholder="getDefaultValue(field)">
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { ClientField } from "@/models";
import {toReadableString} from "../../utils/string";

export default defineComponent({
  methods: {toReadableString},
  props: {
    clientFields: {
      type: Array as () => ClientField[],
      required: true
    },
    editingFields: {
      type: Object as () => { [key: string]: string },
      required: true
    },
    handleInputChange: Function as (field: ClientField) => void,
    getDefaultValue: Function as (field: ClientField) => string
  }
});
</script>
