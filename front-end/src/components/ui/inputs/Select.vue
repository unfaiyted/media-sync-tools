<template>
    <select
        v-model="selectedValue"
        :disabled="isDisabled"
        @change="handleSelectChange"
        class="form-select block w-full mt-1"
        :class="selectClass"
    >
        <option v-for="option in options" :key="option.value" :value="option.value">
            {{ option.text }}
        </option>
    </select>
</template>

<script lang="ts">
import { ref, defineComponent, computed } from 'vue';

export default defineComponent({
    name: 'VSelect',

    props: {
        modelValue: [String, Number],
        options: {
            type: Array,
            required: true
        },
        isDisabled: {
            type: Boolean,
            default: false
        }
    },

    setup(props, { emit }) {
        const selectedValue = ref(props.modelValue);

        const selectClass = computed(() => {
            if(props.isDisabled) {
                return 'opacity-50 cursor-not-allowed';
            }
            return 'cursor-pointer';
        });

        const handleSelectChange = () => {
            emit('update:modelValue', selectedValue.value);
        }

        return {
            selectedValue,
            selectClass,
            handleSelectChange
        }
    }
});
</script>

<style scoped>
/* Additional styling as needed */
</style>
