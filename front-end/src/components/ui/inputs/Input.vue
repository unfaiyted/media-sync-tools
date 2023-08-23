<template>
  <div>
    <label v-if="label" :for="inputId" class="block text-sm font-medium" :class="labelClass">{{ label }}</label>
    <input
        :id="inputId"
        :type="type"
        v-model="inputValue"
        :placeholder="placeholder"
        :disabled="isDisabled"
        @input="handleInputChange"
        class="form-input block w-full mt-1 appearance-none block w-full bg-gray-700 text-white border border-gray-600 rounded py-2 px-4 mb-3 leading-tight focus:outline-none focus:bg-gray-600 focus:border-gray-500"
        :class="[inputClass, themeClass]"
    />
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, computed } from 'vue';

export default defineComponent({
  name: 'VInput',

  props: {
    modelValue: [String, Number],
    placeholder: String,
    type: {
      type: String,
      default: 'text'
    },
    isDisabled: {
      type: Boolean,
      default: false
    },
    theme: {
      type: String,
      default: 'light',
      validator: (value: string) => ['dark', 'light'].includes(value)
    },
    label: {
      type: String,
      default: ''
    }
  },

  setup(props, { emit }) {
    const inputValue = ref(props.modelValue);
    const inputId = ref(`input_${Math.random().toString(36).substr(2, 9)}`); // Unique ID for input

    const inputClass = computed(() => {
      if(props.isDisabled) {
        return 'opacity-50 cursor-not-allowed';
      }
      return 'cursor-pointer';
    });

    const handleInputChange = () => {
      emit('update:modelValue', inputValue.value);
    }

    const themeClass = computed(() => {
      return props.theme === 'light'
          ? 'bg-white text-gray-800 border-gray-400 focus:bg-gray-200 focus:border-gray-500'
          : 'bg-gray-700 text-white border-gray-600 focus:bg-gray-600 focus:border-gray-500';
    });

    const labelClass = computed(() => {
      return props.theme === 'light'
          ? 'text-gray-800'
          : 'text-white';
    });

    return {
      inputValue,
      inputClass,
      themeClass,
        labelClass,
      handleInputChange,
      inputId
    }
  }
});
</script>

<style scoped>
/* Additional styling as needed */
</style>
