// src/stores/posterStore.ts

import { defineStore } from 'pinia';
import {
    IconPosition,
    MediaImageType,
    MediaPoster, MediaPosterBackgroundOptions,
    MediaPosterBorderOptions,
    MediaPosterGradientOptions, MediaPosterIconOptions, MediaPosterOverlayOptions,
    MediaPosterTextOptions
} from "@/models";
import {
    createMediaPoster, fetchPoster, updateMediaPoster, deleteMediaPoster, fetchIcons, fetchBackgroundImages,
    // ... any other required methods ...
} from "@/api/posters";
import {API_URL} from "@/utils/constants";
import {validateColors} from "@/utils/arrays";

interface PosterState {
    mediaPosters: MediaPoster[];
    currentPoster: MediaPoster | null;
    icons: string[];
    backgroundImages: string[];
    loading: boolean;
    error: boolean;
    errorMessage: string;
}

const defaultPoster:  MediaPoster = {
    mediaPosterId: crypto.randomUUID(),
    text: {
        enabled: true,
        text: 'Hello World!',
        // font: 'Arial',
        // size: 24,
        // style: 'normal',
        // weight: 'normal',
        // align: 'left',
        position: [0, 0],
        color: [255, 255, 255],
        shadow: {
            enabled: false,
            color: [0, 0, 0],
            blur: 0,
            offset: 0,
            transparency: 100,
        },
        border: {
            enabled: false,
            color: [0, 0, 0],
            width: 1,
            height: 1,
        },
    },
    width: 400,
    height: 600,
    type: MediaImageType.POSTER,
    gradient: {
        enabled: false,
        colors: [
            [255, 255, 255],
            [0, 0, 0],
            [100,100,100]
        ],
        opacity: 0.5,
        type: 'linear',
        angle: 160
    },
    background: {
        // url: './assets/images/poster-background.jpg',
        enabled: false,
        opacity: 0.5,
        position: [0,0],
        // color: [100, 200, 0],
        border: {
            enabled: true,
            color: [50, 50, 50],
            width: 10,
            height: 10,
        },

    },
    border: {
        enabled: false,
        color: [0, 0, 0],
        width: 5,
        height: 5,
    },
    icon: {
        enabled: false,
        path: '',
        position: IconPosition.MIDDLE,
        size: [200, 250],

    },
    overlays: [{
        enabled: false,
        cornerRadius: 0,
        transparency: 0,
        icon: {
            enabled: true,
            path: '',
            size: [0, 0],
            position: IconPosition.LEFT,
        },
        position: IconPosition.LEFT // Default position, adjust if needed
    }]
}

export const usePosterStore = defineStore({
    id: 'mediaPoster',
    state(): PosterState {
        return {
            mediaPosters: [],
            currentPoster: null,
            icons: [],
            backgroundImages: [],
            loading: true,
            error: false,
            errorMessage: '',
        };
    },
    actions: {
        handleError(err: any) {
            this.error = true;
            this.errorMessage = err.response ? err.response.data.detail : 'An unexpected error occurred';
            this.loading = false;
        },

        asyncWrapper: async function(action: (...args: any[]) => Promise<any>, ...args: any[]) {
            try {
                return await action(...args);
            } catch (err) {
                this.handleError(err);
            } finally {
                if (!this.error) this.loading = false;
            }
        },

        fetchAllPosters: async function(): Promise<MediaPoster[]> {
            this.mediaPosters = await this.asyncWrapper(fetchPoster);
            return this.mediaPosters;
        },

        getPoster: function(posterId: string): MediaPoster | undefined {
            return this.mediaPosters.find(poster => poster.mediaPosterId === posterId);
        },

        addPoster: async function(mediaPoster: MediaPoster) {
            const newPoster = await this.asyncWrapper(createMediaPoster, mediaPoster);
            if (newPoster) this.mediaPosters.push(newPoster);
        },

        updatePoster: async function(updatedMediaPoster: MediaPoster) {
            const updatedPoster = await this.asyncWrapper(updateMediaPoster, updatedMediaPoster);
            const index = this.mediaPosters.findIndex(poster => poster.mediaPosterId === updatedPoster.mediaPosterId);
            if (index >= 0) this.mediaPosters[index] = updatedPoster;
        },

        removePoster: async function(posterId: string) {
            await this.asyncWrapper(deleteMediaPoster, posterId);
            const index = this.mediaPosters.findIndex(poster => poster.mediaPosterId === posterId);
            if (index >= 0) this.mediaPosters.splice(index, 1);
        },

        setCurrentPoster: function(posterId: string) {
            const index = this.mediaPosters.findIndex(poster => poster.mediaPosterId === posterId);
            this.currentPoster = (index >= 0) ? this.mediaPosters[index] : null;
            return this.currentPoster;
        },

        setCurrentPosterFromPoster: function(poster: MediaPoster) {
            this.currentPoster = poster;
            return this.currentPoster;
        },

        resetCurrentPoster: function() {
            this.currentPoster = null;
        },

        setDefaultPoster: function() {
            this.currentPoster = {...defaultPoster};
            return this.currentPoster;
        },


        updateTextOptions: function(textOptions: MediaPosterTextOptions) {
            this.currentPoster!.text = textOptions;
        },

        updateBorderOptions: function(borderOptions: MediaPosterBorderOptions) {
            this.currentPoster!.border = borderOptions;
        },

        updateTextBorderOptions: function(borderOptions: MediaPosterBorderOptions) {
            this.currentPoster!.text!.border = borderOptions;
        },

        updateOverlayBorderOptions: function(borderOptions: MediaPosterBorderOptions) {
            this.currentPoster!.overlays![0].border = borderOptions;
        },

        updateGradientOptions: function(gradientOptions: MediaPosterGradientOptions) {


            this.currentPoster!.gradient = gradientOptions;
        },
        updateBackgroundOptions: function(backgroundOptions: MediaPosterBackgroundOptions) {
            this.currentPoster!.background = backgroundOptions;
        },
        updateIconOptions: function(iconOptions: MediaPosterIconOptions) {
            this.currentPoster!.icon = iconOptions;
        },
        updateOverlayOptions: function(overlayOptions: MediaPosterOverlayOptions) {
            this.currentPoster!.overlays = [overlayOptions];
        },
        associateWithMediaItem: function(mediaItemId: string) {
            this.currentPoster!.mediaItemId = mediaItemId;
        },

        savePoster: async function() {
            if (this.currentPoster) {
                if (this.currentPoster.mediaPosterId) {
                    await this.updatePoster(this.currentPoster);
                } else {
                    await this.addPoster(this.currentPoster);
                }
            }
        },

        createPoster: async function(mediaPoster: MediaPoster) {
                try {
                    mediaPoster.mediaPosterId = crypto.randomUUID();


                    // const validate = Object.assign({}, mediaPoster);

                    // validate.gradient!.colors = validateColors(validate.gradient!.colors);
                    // console.log('validate',validate)
                    const response = await createMediaPoster(mediaPoster);

                    console.log('res', response)
                    // const blob = await response.blob();
                    const url = window.URL.createObjectURL(response.data);

                    if(this.currentPoster)
                        this.currentPoster.url = url;

                    return this.currentPoster;
                } catch (error) {
                    console.error("Error fetching image:", error);
                }
        },


        // list of filesnames
        getBackgroundImages: async function() {
            if(this.backgroundImages.length === 0) this.backgroundImages = await this.asyncWrapper(fetchBackgroundImages);
            return this.backgroundImages;
        },

        toggleText: function(value: boolean | undefined) {
            if((typeof value === 'boolean') && this.currentPoster && this.currentPoster.text) {
                console.log('set', value)
                this.currentPoster.text.enabled = value;
            } else if(this.currentPoster)
                this.currentPoster.text!.enabled = !this.currentPoster.text!.enabled;
        },
        toggleGradient: function(value: boolean | undefined) {
            if((typeof value === 'boolean') && this.currentPoster && this.currentPoster.gradient) {
                console.log('set', value)
                this.currentPoster.gradient.enabled = value;
            } else if(this.currentPoster)
                this.currentPoster.gradient!.enabled = !this.currentPoster.gradient!.enabled;
        },
        toggleBorder: function(value: boolean| undefined) {
            if((typeof value === 'boolean') && this.currentPoster && this.currentPoster.border) {
                console.log('set', value)
                this.currentPoster.border.enabled = value;
            } else if(this.currentPoster)
                this.currentPoster.border!.enabled = !this.currentPoster.border!.enabled;
        },
        toggleBackground: function(value: boolean|undefined) {
            if((typeof value === 'boolean') && this.currentPoster && this.currentPoster.background) {
                console.log('set', value)
                this.currentPoster.background.enabled = value;
            } else if(this.currentPoster)
                this.currentPoster.background!.enabled = !this.currentPoster.background!.enabled;
        },
        toggleOverlay: function(value: boolean|undefined) {
            if((typeof value === 'boolean') && this.currentPoster && this.currentPoster.overlays) {
                console.log('set', value)
                this.currentPoster.overlays[0].enabled = value;
            } else if(this.currentPoster)
                this.currentPoster.overlays![0].enabled = !this.currentPoster.overlays![0].enabled;
        },
        toggleIcon: function(value: boolean|undefined) {
            if((typeof value === 'boolean') && this.currentPoster && this.currentPoster.icon) {
                console.log('set', value)
                this.currentPoster.icon.enabled = value;
            } else if(this.currentPoster)
                this.currentPoster.icon!.enabled = !this.currentPoster.icon!.enabled;
        },
        getIcons: async function() {
            if(this.icons.length === 0) this.icons = await this.asyncWrapper(fetchIcons);
            return this.icons;
        },
        resetState() {
            this.mediaPosters = [];
            this.loading = true;
            this.error = false;
            this.errorMessage = '';
        }
    }
});
