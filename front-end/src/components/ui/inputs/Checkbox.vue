<template>
    <div class="flex items-center">
        <template v-if="labelPosition === 'right'">
            <input :id="id"
                   type="checkbox"
                   v-model="modelValue"
                   :disabled="isDisabled"
                   @change="handleCheckboxChange"
                   class="form-checkbox h-5 w-5 text-blue-600"
                   :class="checkboxClass"
            />
            <label :for="id" class="ml-2 text-gray-700 cursor-pointer">{{ label }}</label>
        </template>

        <template v-else>
            <label :for="id" class="mr-2 text-gray-700 cursor-pointer">{{ label }}</label>
            <input :id="id"
                   type="checkbox"
                   v-model="modelValue"
                   :disabled="isDisabled"
                   @change="handleCheckboxChange"
                   class="form-checkbox h-5 w-5 text-blue-600"
                   :class="checkboxClass"
            />
        </template>
    </div>
</template>



<script lang="ts">
import { ref, defineComponent, computed } from 'vue';

export default defineComponent({
    name: 'VCheckbox',

    props: {
        modelValue: Boolean,
        label: {
            type: String,
            default: ''
        },
        isDisabled: {
            type: Boolean,
            default: false
        },
        labelPosition: {
            type: String,
            default: 'right' // or 'left'
        },
        id: {
            type: String,
            default: ''
        }
    },

    setup(props, { emit }) {
        const checkboxClass = computed(() => {
            if(props.isDisabled) {
                return 'opacity-50 cursor-not-allowed';
            }
            return 'cursor-pointer';
        });

        const handleCheckboxChange = (event: Event) => {
            emit('update:modelValue', (event.target as HTMLInputElement).checked);
        }

        return {
            checkboxClass,
            handleCheckboxChange
        }
    }
});
</script>

<style scoped>
/* Additional styling as needed */
</style>
