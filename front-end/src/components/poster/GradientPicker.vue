<template>
    <div>
        <label for="gradientColors">Choose Gradient:</label>
        <select id="gradientColors" v-model="selectedGradient">
            <option v-for="(value, key) in gradientColors" :key="key" :value="key">
                {{ key }}
            </option>
            <option value="random">Random</option>
        </select>
    </div>

    <div>
        <label for="angleSlider">Angle: {{ angle }}°</label>
        <input type="range" v-model="angle" min="-180" max="180" id="angleSlider" />
    </div>


    <!-- Other component code -->
    <div>
        <label for="gradientColor1">Color 1:</label>
        <picker v-model:pureColor="gradientColor1" @input="handleChange"/>
        {{ gradientColor1 }}
    </div>

    <div>
        <label for="gradientColor2">Color 2:</label>
<!--        <picker v-model="gradientColor2" @input="handleColorChange" /> {{gradientColor2}}-->

        <picker v-model:pureColor="gradientColor2" @input="handleChange"/>

        {{ gradientColor2 }}
    </div>

    <!-- Other component code -->
</template>

<script>
import { ColorPicker } from "vue3-colorpicker";
import "vue3-colorpicker/style.css";
import {parseRGB} from "@/utils/string";



const gradientColors = {
    'red-darkred': [[255, 0, 0], [128, 0, 0]],
    'green-darkgreen': [[0, 255, 0], [0, 128, 0]],
    'blue-darkblue': [[0, 0, 255], [0, 0, 128]],
    'yellow-olive': [[255, 255, 0], [128, 128, 0]],
    'cyan-teal': [[0, 255, 255], [0, 128, 128]],
    'magenta-purple': [[255, 0, 255], [128, 0, 128]],
    'orange-darkorange': [[255, 165, 0], [128, 83, 0]],
    'maroon-darkmaroon': [[128, 0, 0], [64, 0, 0]],
    'olive-darkolive': [[128, 128, 0], [64, 64, 0]],
    'darkgreen-verydarkgreen': [[0, 128, 0], [0, 64, 0]],
    'grey-darkgrey': [[128, 128, 128], [64, 64, 64]],
    'white-grey': [[255, 255, 255], [128, 128, 128]]
};


export default {
    components: {
        'picker': ColorPicker,
    },
    data() {
        return {
            gradientColor1: 'rgb(255,255,255)',
            gradientColor2: 'rgb(0,0,0)',
            angle: -160,
            gradientColors: gradientColors,
            selectedGradient: 'random',

            // ... other data properties
        };
    },
    watch: {
        gradientColor1: 'handleChange',
        gradientColor2: 'handleChange',
        selectedGradient: 'handleNamedGradientChange', // TODO: implement this
        angle: 'handleChange',
    },
    methods: {
        handleChange(change) {
            console.log('Gradient changed', change);
            this.$emit('gradient-changed', { gradientColor1: parseRGB(this.gradientColor1),
                gradientColor2: parseRGB(this.gradientColor2), angle: this.angle, selectedGradient: this.selectedGradient });
        },
        handleNamedGradientChange(change) {
            console.log('Named gradient changed', change);
            this.$emit('gradient-changed', { gradientColor1: null,
                gradientColor2: null, angle: this.angle, selectedGradient: this.selectedGradient });
        },
    },
};
</script>

