<template>
    <input
        :type="type"
        v-model="inputValue"
        :placeholder="placeholder"
        :disabled="isDisabled"
        @input="handleInputChange"
        class="form-input block w-full"
        :class="inputClass"
    />
</template>

<script lang="ts">
import { ref, defineComponent, computed } from 'vue';

export default defineComponent({
    name: 'InputComponent',

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
        }
    },

    setup(props, { emit }) {
        const inputValue = ref(props.modelValue);

        const inputClass = computed(() => {
            if(props.isDisabled) {
                return 'opacity-50 cursor-not-allowed';
            }
            return 'cursor-pointer';
        });

        const handleInputChange = () => {
            emit('update:modelValue', inputValue.value);
        }

        return {
            inputValue,
            inputClass,
            handleInputChange
        }
    }
});
</script>

<style scoped>
/* Additional styling as needed */
</style>
