<template>
    <div class="container">
        <!-- Search and Button -->
        <div class="controls">
            <input v-model="searchQuery" placeholder="Enter search term" class="search-input" />
            <TextEffects/>
            <button @click="fetchImage" class="search-button">Create Poster</button>

        </div>

        <!-- Poster Display -->
        <div class="poster">
            <img v-if="posterImage" :src="posterImage" alt="Poster" />
        </div>

        <!-- Controls Below Poster -->
        <div class="sliders">

            <BorderColorPicker @border-changed="updateBorder"></BorderColorPicker>
            <GradientColorPickers @gradient-changed="updateGradient"></GradientColorPickers>
            <IconPicker @icon-selected="updateIcon"></IconPicker>
            <DragDrop @background-image-selected="updateBgImage"/>
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.search-input {
    padding: 10px;
    font-size: 16px;
    border-radius: 5px;
    border: 1px solid #ddd;
    flex: 1;
    margin-right: 10px;
}

.search-button {
    padding: 10px 20px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

.search-button:hover {
    background-color: #0056b3;
}

.poster {
    width: 400px;
    height: 600px;
    background-color: #f2f2f2;
    margin: 20px auto;
    position: relative;
}

.poster img {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
}

.sliders > div {
    margin-bottom: 20px;
}
</style>

<script>
// import { debounce } from 'lodash';

import GradientColorPickers from "@/components/GradientPicker.vue";
import BorderColorPicker from "@/components/BorderColorPicker.vue";
import IconPicker from "@/components/IconPicker.vue";
import DragDrop from "@/components/DragDrop.vue";
import TextEffects from "@/components/TextEffects.vue";
import {API_URL} from "@/utils/constants";


export default {
    components: {TextEffects, DragDrop, BorderColorPicker, GradientColorPickers, IconPicker},
    data() {
        return {
            searchQuery: 'Hi!',
            posterImage: null,
            border: null,
            gradient: null,

            icon: null,
            angle: -160,
        };
    },
    watch: {
        border: 'fetchImage',
        searchQuery: 'fetchImage',
        gradient: 'fetchImage',
        bgImage: 'fetchImage',
        icon: 'fetchImage',
        angle: 'fetchImage',
    },
    methods: {
        updateBgImage(image) {
            this.bgImage = image.backgroundImage;
            this.fetchImage();
        },
        updateGradient(changes) {
            this.gradient = {
                ...this.gradient,
                ...changes
            }

            this.fetchImage();
        },
        updateBorder(changes) {
            this.border = {
                ...this.border,
                ...changes
            }

            this.fetchImage();
        },
        updateIcon(icon) {
            this.icon = icon.icon;
            this.fetchImage();
        },
        async fetchImage() {
            try {

                const request = {
                    query: this.searchQuery,
                    bgImage: this.bgImage,
                    angle: this.angle,
                    icon: this.icon,
                    ...this.border,
                    ...this.gradient,
                }

                console.log(request)

                const response = await fetch(`${API_URL}/image/poster/create`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },

                    body: JSON.stringify(request)
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                this.posterImage = url;

            } catch (error) {
                console.error("Error fetching image:", error);
            }
        }
    }
}
</script>
