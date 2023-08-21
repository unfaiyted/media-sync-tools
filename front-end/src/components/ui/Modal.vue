<template>
  <transition name="fade" enter-active-class="transition-opacity duration-300" leave-active-class="transition-opacity duration-300" enter-class="opacity-0" enter-to-class="opacity-100" leave-class="opacity-100" leave-to-class="opacity-0">
    <div v-if="isOpen" class="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-gray-800 p-5 rounded-lg shadow-lg w-3/4 max-w-xl z-50">
      <slot></slot>
      <div class="flex justify-end">
          <button @click="doAction" :class="buttonClass">
              <span v-if="buttonState === 'idle'">{{ doActionText }}</span>
              <svg v-if="buttonState === 'loading'" class="animate-spin -ml-1 mr-3 h-5 w-5  text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <CheckIcon v-if="buttonState === 'success'" class="h-5 w-5 text-white" />
          </button>

          <button @click="cancelAction" class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">{{cancelActionText}}</button>
      </div>
    </div>
  </transition>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue';
import { CheckIcon } from "@heroicons/vue/24/outline";

enum ButtonState {
    idle = 'idle',
    loading = 'loading',
    success = 'success'
}


export default defineComponent({
  name: 'Modal',
    components: {
        CheckIcon
    },
  props: {
      isOpen: Boolean,
      // doAction: Function,
      // cancelAction: Function,
      doActionText: {
          type: String,
          default: 'Continue'
      },
      cancelActionText: {
          type: String,
          default: 'Cancel'
      },
  },
    data() {
     return {
         buttonState: ButtonState.idle
     };
    },
  methods: {
    async doAction() {
        this.buttonState = ButtonState.loading;
      this.$emit('do-action');

      await new Promise((resolve) => setTimeout(resolve, 1000)); // replace this with your actual API call
        this.buttonState = ButtonState.success;

        setTimeout(() => {
            this.$emit('cancel-action', false);
            this.buttonState = ButtonState.idle
        }, 750);

    },
    cancelAction() {
      this.$emit('cancel-action', false);
    }
  },
  computed: {
    buttonClass() {
      return {
        'bg-indigo-600': this.buttonState === ButtonState.idle,
        'bg-gray-500': this.buttonState !== ButtonState.idle,
        'text-white': true,
        'flex px-4 min-w-[25%] mr-2 justify-center items-center': true,
        'py-2': true,
        'rounded': true,
        'hover:bg-indigo-700': this.buttonState === ButtonState.idle,
        'cursor-not-allowed': this.buttonState !== ButtonState.idle,
      };
    },
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
