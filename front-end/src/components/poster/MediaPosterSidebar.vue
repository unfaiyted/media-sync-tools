<template>
    <div class="flex">
        <!-- Sidebar -->
        <div
            :class="['bg-gray-700 p-4  overflow-y-auto', isCollapsed ? 'w-20' : 'w-80']"
            style="max-height: calc(100vh - 0px);">


          <!-- Buttons Container -->
          <div class="flex justify-end  mb-4 ">
<!--            <VButton-->
<!--                class="text-white"-->
<!--                @click="toggleSidebar"-->
<!--                :label="isCollapsed ? '>>' : '<<'"-->
<!--            ></VButton>-->

            <VButton
                class="text-white"
                label="Create Poster"
            ></VButton>
          </div>

          <!-- Place your sidebar content here -->
          <div v-if="!isCollapsed">
            <VAccordion :items="accordionItems" />
          </div>
        </div>


      <!-- Main Content -->
        <div class="flex-grow">
            <!-- Your main content goes here -->
        </div>
    </div>
</template>


<script lang="ts">
import PosterImage from "@/components/poster/PosterImage.vue";
import MediaPosterTextOptions from "@/components/poster/MediaPosterTextOptions.vue";
import {IconPosition, MediaImageType, MediaPoster} from "@/models";
import MediaPosterGradientOptions from "@/components/poster/MediaPosterGradientOptions.vue";
import MediaPosterBackgroundOptions from "@/components/poster/MediaPosterBackgroundOptions.vue";
import MediaPosterIconOptions from "@/components/poster/MediaPosterIconOptions.vue";
import MediaPosterBorderOptions from "@/components/poster/MediaPosterBorderOptions.vue";
import MediaPosterOverlayOptions from "@/components/poster/MediaPosterOverlays.vue";
import {ref} from "vue";
import VButton from "@/components/ui/inputs/Button.vue";
import VAccordion from "@/components/ui/Accordian.vue";



export default defineComponent({
    name: "MediaPosterSidebar",
    components: {
      VAccordion,
      VButton,
        MediaPosterBackgroundOptions,
        MediaPosterGradientOptions,
        MediaPosterTextOptions,
        MediaPosterIconOptions,
        MediaPosterOverlayOptions,
        MediaPosterBorderOptions,

        // EndpointTrigger,
        /*PlaylistEditor*/
        PosterImage
    },
    methods: {
    },
    setup(props) {
        const poster = ref<MediaPoster>({
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
                    enabled: true,
                    color: [0, 0, 0],
                    blur: 0,
                    offset: 0,
                    transparency: 100,
                },
                border: {
                    enabled: true,
                    color: [0, 0, 0],
                    width: 1,
                    height: 1,
                },
            },
            width: 400,
            height: 600,
            type: MediaImageType.POSTER,
            gradient: {
                enabled: true,
                colors: [
                    [255, 255, 255],
                    [0, 0, 0],
                ],
                opacity: 0.5,
                type: 'linear',
                angle: 0
            },
            background: {
                url: '',
                enabled: true,
                opacity: 1.0,
                color: [0, 0, 0],
                border: {
                    enabled: true,
                    color: [0, 0, 0],
                    width: 1,
                    height: 1,
                },

            },
            border: {
                enabled: true,
                color: [0, 0, 0],
                width: 1,
                height: 1,
            },
            icon: {
                enabled: true,
                path: '',
                position: IconPosition.MIDDLE,
                size: [200, 250],

            },
            overlays: [{
                enabled: true,
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
        });

        const isCollapsed = ref(false);

        const toggleSidebar = () => {
            isCollapsed.value = !isCollapsed.value;
        };

      const accordionItems = ref([
        {
          title: 'Text Options',
          component: MediaPosterTextOptions,
          enabled: poster.value.text.enabled,
          props: { value: poster.value.text }
        },
        {
          title: 'Gradient Options',
          enabled: false,
          component: MediaPosterGradientOptions,
          props: { gradientOptions: poster.value.gradient }
        },
        {
          title: 'Background Options',
          enabled: false,
          component: MediaPosterBackgroundOptions,
          props: { value: poster.value.background }
        },
        {
          title: 'Border Options',
          enabled: false,
          component: MediaPosterBorderOptions,
          props: { border: poster.value.border }
        },
        {
          title: 'Icon Options',
          enabled: false,
          component: MediaPosterIconOptions,
          props: { iconOptions: poster.value.icon }
        },
        {
          title: 'Overlay Options',
          enabled: poster.value.overlays.length > 0,
          component: MediaPosterOverlayOptions,
          props: { overlayOptions: poster.value.overlays }
        }
      ]);


      return {
        isCollapsed,
        toggleSidebar,
        poster,
        accordionItems
      };

    }
});
</script>

<style>
.overflow-y-auto {
    scroll-behavior: smooth;
}

.overflow-y-auto::-webkit-scrollbar {
    width: 8px;
}
.overflow-y-auto::-webkit-scrollbar-thumb {
    background-color: rgba(255, 255, 255, 0.5);
    border-radius: 4px;
}
.overflow-y-auto::-webkit-scrollbar-track {
    background-color: rgba(255, 255, 255, 0.1);
}


</style>
