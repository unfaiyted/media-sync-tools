<template>
    <div>
        <h3>Shadow Options</h3>

        <div>
            <label for="shadowOffsetX">Offset X:</label>
            <input id="shadowOffsetX" v-model="shadow.offsetX" type="number" placeholder="Enter shadow X offset" />
        </div>

        <div>
            <label for="shadowOffsetY">Offset Y:</label>
            <input id="shadowOffsetY" v-model="shadow.offsetY" type="number" placeholder="Enter shadow Y offset" />
        </div>

        <div>
            <label for="shadowBlur">Blur:</label>
            <input id="shadowBlur" v-model="shadow.blur" type="number" placeholder="Enter shadow blur" />
        </div>

        <div>
            <label for="shadowColor">Color:</label>
            <input id="shadowColor" v-model="shadow.color" type="color" placeholder="Select shadow color" />
        </div>
    </div>
</template>

<script>
export default {
    name: "MediaPosterShadowOptions",
    data() {
        return {
            shadow: {
                offsetX: 0,  // Default X offset
                offsetY: 0,  // Default Y offset
                blur: 5, // Default blur
                color: '#000000', // Default color
            }
        };
    }
};
</script>

<style scoped>
/* You can add any specific styles for this component here */
</style>
