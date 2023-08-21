<template>
  <transition name="fade" enter-active-class="transition-opacity duration-300" leave-active-class="transition-opacity duration-300" enter-class="opacity-0" enter-to-class="opacity-100" leave-class="opacity-100" leave-to-class="opacity-0">
    <div v-if="isOpen" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-800 p-5 rounded-lg shadow-lg w-3/4 max-w-xl z-50">
      <slot></slot>
      <div class="flex justify-end">
        <button @click="doAction" class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 mr-2">Request</button>
        <button @click="cancelAction" class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">Cancel</button>
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
  name: 'Modal',
  props: {
    isOpen: Boolean,
    doAction: Function,
    cancelAction: Function,
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = 'auto';
      }
    },
  },
});
</script>
