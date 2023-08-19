<template>
    <div>
        <h3>Border Options</h3>

        <div>
            <label for="borderWidth">Width:</label>
            <input id="borderWidth" v-model="border.width" type="number" placeholder="Enter border width" />
        </div>

        <div>
            <label for="borderColor">Color:</label>
            <input id="borderColor" v-model="border.color" type="color" placeholder="Select border color" />
        </div>

        <div>
            <label for="borderStyle">Style:</label>
            <select id="borderStyle" v-model="border.style">
                <option value="solid">Solid</option>
                <option value="dashed">Dashed</option>
                <option value="dotted">Dotted</option>
                <option value="double">Double</option>
                <!-- Add other styles as needed -->
            </select>
        </div>
    </div>
</template>

<script>
export default {
    name: "MediaPosterBorderOptions",
    data() {
        return {
            border: {
                width: 1,  // Default width
                color: '#000000', // Default color
                style: 'solid' // Default style
            }
        };
    }
};
</script>

<style scoped>
/* You can add any specific styles for this component here */
</style>
