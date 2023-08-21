<template>
    <!-- Other component code -->
    <div>
        <label for="borderWidth">Border Width: {{ borderWidth }}</label>
        <input type="range" id="borderWidth" v-model="borderWidth" min="0" max="50">
    </div>

    <div>
        <label for="borderHeight">Border Height: {{ borderHeight }}</label>
        <input type="range" id="borderHeight" v-model="borderHeight" min="0" max="50">
    </div>

    <div>
        <label for="borderColor">Border Color:</label>
        <picker v-model:pureColor="borderColor"  @input="handleChange"/>
       {{borderColor}}
    </div>

</template>

<script>
import { ColorPicker } from "vue3-colorpicker";
import "vue3-colorpicker/style.css";
import {parseRGB} from "@/utils/string";
export default {
    components: {
        'picker': ColorPicker,
    },
    data() {
        return {
            borderColor: 'rgb(0, 0, 0)',
            borderWidth: 0,
            borderHeight: 0,
            // ... other data properties
        };
    },
    watch: {
        borderColor: 'handleChange',
        borderWidth: 'handleWidthChange',
        borderHeight: 'handleHeightChange',

    },
    methods: {
        handleChange() {
            this.$emit('border-changed', { borderColor: parseRGB(this.borderColor) });
        },
        handleWidthChange() {
            this.$emit('border-changed', { borderWidth: this.borderWidth });
        },
        handleHeightChange() {
            this.$emit('border-changed', { borderHeight: this.borderHeight });
        },
    },
};
</script>

