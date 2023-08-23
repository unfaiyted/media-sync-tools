<template>
  <div class="flex items-center">
    <label :for="id" class="font-semibold mr-4">{{ label }}</label>
    <label class="switch">
      <input
          type="checkbox"
          v-model="toggleValue"
          :disabled="isDisabled"
          @change="handleToggleChange"
          class="hidden"
          :id="id"
      >
      <span class="slider round"></span>
    </label>
  </div>
</template>


<script lang="ts">
import { ref, defineComponent, computed, toRefs } from 'vue';

export default defineComponent({
    name: 'VToggle',

    props: {
        modelValue: Boolean,
        label: String,
        isDisabled: {
            type: Boolean,
            default: false,
        },
    },

    setup(props, { emit }) {
        const { modelValue, isDisabled } = toRefs(props);
        const toggleValue = ref(modelValue.value);

        const id = `toggle-${Math.random().toString(36).substr(2, 9)}`;



        const toggleClass = computed(() => {
            return isDisabled.value
                ? 'bg-gray-200 cursor-not-allowed'
                : toggleValue.value
                    ? 'bg-indigo-600'
                    : 'bg-gray-400';
        });

      const thumbClass = computed(() => {
    return toggleValue.value
        ? 'translate-x-4'
        : 'translate-x-0';
      });

        const handleToggleChange = () => {
            emit('update:modelValue', toggleValue.value);
        };

        return {
            toggleValue,
          thumbClass,
            toggleClass,
            handleToggleChange,
            id,
        };
    },
});
</script>

<style scoped>
.toggle-thumb {
    transform: translateX(0);
    transition: transform 0.2s ease-in;
}


.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(20px);
  -ms-transform: translateX(20px);
  transform: translateX(20px);
}
</style>
