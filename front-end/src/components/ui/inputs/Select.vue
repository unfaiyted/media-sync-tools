<template>
  <div :class="wrapperClass">
    <label v-if="label" :for="selectId" class="select-label ">{{ label }}</label>
    <select
        :id="selectId"
        v-model="selectedValue"
        :disabled="isDisabled"
        @change="handleSelectChange"
        class="form-select block w-full mt-1"
        :class="selectClass"
    >
      <option v-for="option in parsedOptions" :key="option.value" :value="option.value">
        {{ option.text }}
      </option>
    </select>
  </div>
</template>

<script lang="ts">



import { ref, defineComponent, computed } from 'vue';
import {SelectOption} from "@/models/ui";

export default defineComponent({
  name: 'VSelect',

  props: {
    modelValue: [String, Number],
    options: {
      type: Object as () => SelectOption[] | string,
      required: true
    },
    isDisabled: {
      type: Boolean,
      default: false
    },
    theme: {
      type: String,
      default: 'dark',
      validator: (value:string) => ['light', 'dark'].includes(value)
    },
    label: {
      type: String,
      default: ''
    },
    labelPosition: {
      type: String,
      default: 'top',
      validator: (value: string) => ['left', 'right', 'top', 'bottom'].includes(value)
    }
  },

  setup(props, { emit }) {
    const selectedValue = ref(props.modelValue);
    const selectId = ref(`select_${Math.random().toString(36).slice(2,11)}`);

    const selectClass = computed(() => {
      if(props.isDisabled) {
        return 'opacity-50 cursor-not-allowed';
      }
      return 'cursor-pointer';
    });


    const parsedOptions = computed(() => {
      if (typeof props.options === 'string') {
        const results = props.options.split(',').map(option => ({ value: option.trim(), text: option.trim() }));
        console.log(results)
        return results
      }
      return props.options; // Assuming it's already in the format [{ value: 'solid', text: 'solid' }, ...]
    });


    const wrapperClass = computed(() => {
      switch (props.labelPosition) {
        case 'left':
          return 'flex items-center';
        case 'right':
          return 'flex items-center flex-row-reverse';
        case 'bottom':
          return 'flex flex-col-reverse items-start';
        default:
          return 'flex flex-col items-start';
      }
    });

    const handleSelectChange = () => {
      emit('update:modelValue', selectedValue.value);
    }

    const themeClass = computed(() => {
      return props.theme === 'light' ? 'bg-white' : 'bg-gray-800';
    });

    const labelClass = computed(() => {
      const baseClass = 'select-label margin: 0 0.5rem;';
      return props.theme === 'light' ? `${baseClass} text-black` : `${baseClass} text-white`;
    });

    const selectInputClass = computed(() => {
      const baseClasses = selectClass.value;
      const themeClasses = props.theme === 'light' ? 'bg-white text-black border-gray-300' : 'bg-gray-800 text-white border-gray-600';
      return [baseClasses, themeClasses];
    });

    return {
      selectedValue,
      parsedOptions,
      selectClass,
      handleSelectChange,
      selectId,
      wrapperClass,
      themeClass,
      labelClass,
      selectInputClass
    };
  }
});
</script>

<style scoped>
.select-label {
  margin: 0 0.5rem;
}
</style>
