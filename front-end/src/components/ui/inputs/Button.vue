<template>
    <button
        class="p-2 rounded"
        :class="buttonClass"
        :disabled="isDisabled || isLoading"
        @click="handleClick"
    >
        <span v-if="isLoading" class="spinner"></span>
        <span v-else>{{ label }}</span>
    </button>
</template>

<script lang="ts">
import { ref, defineComponent, computed } from 'vue';

export default defineComponent({
    name: 'VButton',

    props: {
        label: {
            type: String,
            default: 'Click me'
        },
        variant: {
            type: String,
            default: 'primary'
        },
        isLoading: {
            type: Boolean,
            default: false
        },
        isDisabled: {
            type: Boolean,
            default: false
        }
    },

    setup(props, { emit }) {
        const buttonClass = computed(() => {
            switch(props.variant) {
                case 'primary':
                    return 'bg-blue-500 hover:bg-blue-600 text-white';
                case 'secondary':
                    return 'bg-gray-500 hover:bg-gray-600 text-white';
                default:
                    return 'bg-gray-300 hover:bg-gray-400 text-black';
            }
        });

        const handleClick = () => {
            if(!props.isDisabled && !props.isLoading) {
                emit('click');
            }
        }

        return {
            buttonClass,
            handleClick
        }
    }
});
</script>

<style>
/* Simple spinner styling for demo purposes */
.spinner {
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top: 2px solid white;
    width: 16px;
    height: 16px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
