<template>
    <div>
        <label>
            Poster Text:
            <input v-model="text" />
        </label>
        <label>
            Text Color:
            <ColorPicker v-model="color" />
        </label>
        <label>
            Border Size:
            <input type="number" v-model.number="borderSize" />
        </label>
        <label>
            Border Color:
            <ColorPicker v-model="borderColor" />
        </label>
        <label>
            Shadow Offset:
            <input type="number" v-model.number="shadowOffset" />
        </label>
        <label>
            Shadow Color:
            <ColorPicker v-model="shadowColor" />
        </label>
        <label>
            Shadow Blur Radius:
            <input type="number" v-model.number="shadowBlurRadius" />
        </label>
        <label>
            Shadow Opacity:
            <input type="range" min="0" max="255" v-model.number="shadowOpacity" />
        </label>
        <button @click="applyEffects">Apply Effects</button>
    </div>
</template>

<script>
// import { ref } from 'vue';
import { ColorPicker } from "vue3-colorpicker";

export default {
    components: {
        ColorPicker
    },
    data() {
        return {
            text: '',
            color: 'rgb(0,0,0)',
            borderSize: 2,
            borderColor: 'rgb(0,0,0)',
            shadowOffset: 4,
            shadowColor: 'rgb(0,0,0)',
            shadowBlurRadius: 3,
            shadowOpacity: 128
        };
    },
    methods: {
        applyEffects() {
            console.log(this.text, this.color, this.borderSize, this.borderColor, this.shadowOffset, this.shadowColor, this.shadowBlurRadius, this.shadowOpacity);
        }
    }
}
</script>


<style scoped>
label {
    display: block;
    margin-bottom: 10px;
}
</style>
