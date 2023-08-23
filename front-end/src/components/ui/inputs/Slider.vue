<template>
    <div :class="wrapperClass">
        <label v-if="(label || icon ) && (labelPosition === 'left' || labelPosition === 'top')"
               :for="sliderId"
               :class="labelClass">
            <component v-if="IconComponent" :is="IconComponent" class="icon-class"/>
            {{ label }}</label>
        <div class="relative mb-4 w-full">
            <input
                :id="sliderId"
                type="range"
                v-model="sliderValue"
                :min="min"
                :max="max"
                :step="step"
                :disabled="isDisabled"
                @input="handleSlide"
                class="slider w-full"
                :class="sliderInputClass"
            />
            <div v-if="showValue" :class="valueClass">
                {{ sliderValue }}
            </div>
        </div>
        <label v-if="label && (labelPosition === 'right' || labelPosition === 'bottom')"
               :for="sliderId"
               :class="labelClass">{{ label }}</label>
    </div>
</template>


<script lang="ts">
import {ref, defineComponent, computed} from 'vue';
import * as HeroIcons from '@heroicons/vue/24/outline';


export default defineComponent({
    name: 'VSlider',

    props: {
        modelValue: Number,
        min: {
            type: Number,
            default: 0
        },
        icon: {
            type: String,
            default: ''
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
        },
        label: {
            type: String,
            default: ''
        },
        theme: {
            type: String,
            default: 'light',
            validator: (value: string) => ['dark', 'light'].includes(value)
        },
        labelPosition: {
            type: String,
            default: 'top',
            validator: (value: string) => ['left', 'right', 'top', 'bottom'].includes(value)
        }
    },

    setup(props, {emit}) {
        const sliderValue = ref(props.modelValue);
        const sliderId = ref(`slider_${Math.random().toString(36).substr(2, 9)}`);

        const sliderClass = computed(() => {
            if (props.isDisabled) {
                return 'opacity-50 cursor-not-allowed';
            }
            return 'cursor-pointer';
        });

        const wrapperClass = computed(() => {
            if (['left', 'right'].includes(props.labelPosition)) {
                return 'flex items-center';
            }
            return '';
        });

        const handleSlide = () => {
            emit('update:modelValue', sliderValue.value);
        }

        const labelClass = computed(() => {
            const labelC = props.theme === 'light' ? 'text-black' : 'text-white ';
            if (['left', 'right'].includes(props.labelPosition)) {
                return `${labelC} mr-2`;
            }

            return labelC
        });

        const sliderInputClass = computed(() => {
            const baseClasses = sliderClass.value;
            const themeClasses = props.theme === 'light' ? 'bg-gray-300' : 'bg-gray-700';
            return [baseClasses, themeClasses];
        });

        const valueClass = computed(() => {
            return props.theme === 'light' ? 'text-black' : 'text-white';
        });


        const iconClass = computed(() => {
            return props.theme === 'light' ? 'text-black' : 'text-white';
        });

        const IconComponent = computed(() => {
            if (props.icon && HeroIcons[props.icon]) {
                console.log('icon', props.icon)
                return HeroIcons[props.icon];
            }
            return null;
        });


        return {
            sliderValue,
            sliderClass,
            handleSlide,
            sliderId,
            wrapperClass,
            labelClass,
            IconComponent,
            iconClass,
            sliderInputClass,
            valueClass
        };
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
    opacity: 0.8;
    transition: opacity 0.2s;
    cursor: pointer;
    margin-top: 5px;
}

.slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 1rem;
    height: 1rem;
    background: #4CAF50;
    border-radius: 50%;
    cursor: pointer;
}

.slider::-ms-track {
    background: none;
    border-color: transparent;
    border-width: 0.5rem 0;
    color: transparent;
    width: 100%;
    height: 0.5rem;
}
/* For IE */
.slider::-ms-thumb {
    appearance: none;
    width: 1rem;
    height: 1rem;
    background: #4CAF50;
    border-radius: 50%;
    cursor: pointer;
}

.slider::-ms-track {
    /* ... other styles ... */
    background: transparent;
}

.icon-class {
    width: 15px;
    transform: translateY(-5px);
}
</style>
