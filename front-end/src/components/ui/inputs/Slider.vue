<template>
    <div class="relative">
        <input
            type="range"
            v-model="sliderValue"
            :min="min"
            :max="max"
            :step="step"
            :disabled="isDisabled"
            @input="handleSlide"
            class="slider"
            :class="sliderClass"
        />
        <div v-if="showValue" class="absolute top-0 left-0 transform translate-x-full translate-y-[-1.5rem] text-center w-8">
            {{ sliderValue }}
        </div>
    </div>
</template>

<script lang="ts">
import { ref, defineComponent, computed } from 'vue';

export default defineComponent({
    name: 'SliderComponent',

    props: {
        modelValue: Number,
        min: {
            type: Number,
            default: 0
        },
        max: {
            type: Number,
            default: 100
        },
        step: {
            type: Number,
            default: 1
        },
        isDisabled: {
            type: Boolean,
            default: false
        },
        showValue: {
            type: Boolean,
            default: false
        }
    },

    setup(props, { emit }) {
        const sliderValue = ref(props.modelValue);

        const sliderClass = computed(() => {
            if(props.isDisabled) {
                return 'opacity-50 cursor-not-allowed';
            }
            return 'cursor-pointer';
        });

        const handleSlide = () => {
            emit('update:modelValue', sliderValue.value);
        }

        return {
            sliderValue,
            sliderClass,
            handleSlide
        }
    }
});
</script>

<style scoped>
.slider {
    /* Additional styling as needed */
    appearance: none;
    width: 100%;
    height: 0.5rem;
    background: #d3d3d3;
    outline: none;
    opacity: 0.7;
    transition: opacity 0.2s;
    cursor: pointer;
}
.slider:hover {
    opacity: 1;
}
.slider::-webkit-slider-thumb {
    appearance: none;
    width: 1rem;
    height: 1rem;
    background: #4CAF50;
    cursor: pointer;
}
.slider::-moz-range-thumb {
    width: 1rem;
    height: 1rem;
    background: #4CAF50;
    cursor: pointer;
}
</style>
