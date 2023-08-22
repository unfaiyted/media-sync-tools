<template>
    <div class="flex items-center">
        <input
            type="checkbox"
            v-model="toggleValue"
            :disabled="isDisabled"
            @change="handleToggleChange"
            class="hidden"
            :id="id"
        />
        <label
            :for="id"
            :class="toggleClass"
            class="relative inline-block w-10 mr-2 transition transform bg-gray-400 rounded-full cursor-pointer h-6"
        >
      <span
          :class="{ 'translate-x-4': toggleValue, 'translate-x-0': !toggleValue }"
          class="absolute inset-y-0 left-0 w-6 h-6 transition-transform bg-white border-2 border-transparent rounded-full shadow toggle-thumb"
      ></span>
        </label>
        <label v-if="label" class="cursor-pointer" :for="id">{{ label }}</label>
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

        const handleToggleChange = () => {
            emit('update:modelValue', toggleValue.value);
        };

        return {
            toggleValue,
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
</style>
