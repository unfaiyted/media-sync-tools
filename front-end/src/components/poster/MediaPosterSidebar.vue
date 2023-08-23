<template>
    <div class="flex">
        <!-- Sidebar -->
        <div
            :class="['bg-gray-700 p-4  overflow-y-auto', isCollapsed ? 'w-20' : 'w-80']"
            style="max-height: calc(100vh - 0px);">

          <!-- Buttons Container -->
          <div class="flex justify-end  mb-4 ">


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
import {PropType, ref} from "vue";
import VButton from "@/components/ui/inputs/Button.vue";
import VAccordion from "@/components/ui/Accordian.vue";
import {usePosterStore} from "@/store/posterStore";



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
    props: {
        poster: { type: Object as PropType<MediaPoster>, required: false },
    },
    setup(props) {
        const store = usePosterStore();
        const poster = ref<MediaPoster>(props.poster || store.setDefaultPoster());
        const isCollapsed = ref(false);

        const toggleSidebar = () => {
            isCollapsed.value = !isCollapsed.value;
        };


      const accordionItems = ref([
        {
          title: 'Text Options',
          component: MediaPosterTextOptions,
          enabled: poster?.value?.text?.enabled || true,
          props: { value: poster.value.text }
        },
        {
          title: 'Gradient Options',
          enabled: poster.value.gradient.enabled,
          component: MediaPosterGradientOptions,
          props: { gradientOptions: poster.value.gradient }
        },
        {
          title: 'Background Options',
          enabled: poster.value.background.enabled,
          component: MediaPosterBackgroundOptions,
          props: { value: poster.value.background }
        },
        {
          title: 'Border Options',
          enabled: poster.value.border.enabled,
          component: MediaPosterBorderOptions,
          props: { border: poster.value.border }
        },
        {
          title: 'Icon Options',
          enabled: poster.value.icon.enabled,
          component: MediaPosterIconOptions,
          props: { iconOptions: poster.value.icon }
        },
        {
          title: 'Overlay Options',
          enabled: false,
          component: MediaPosterOverlayOptions,
          props: { overlayOptions: poster.value.overlays }
        }
      ]);

        const lastAccordionItems = ref(JSON.stringify(accordionItems.value));


        watch(accordionItems, (newVal) => {
            const store = usePosterStore();

            if (JSON.stringify(newVal) !== lastAccordionItems.value) {
                newVal.forEach((item) => {
                    console.log('ITEM:::',item)
                    updateStoreBasedOnComponentName(item, store);
                });

                // Update the lastAccordionItems value
                lastAccordionItems.value = JSON.stringify(newVal);
            }
        }, {deep: true});

        function updateStoreBasedOnComponentName(item: any, store: any) {
            console.log('BEFORE CHANGES',item);

            const mappings: Record<string, (enabled: boolean) => void> = {
                'MediaPosterTextOptions': store.toggleText,
                'MediaPosterGradientOptions': store.toggleGradient,
                'MediaPosterBackgroundOptions': store.toggleBackground,
                'MediaPosterBorderOptions': store.toggleBorder,
                'MediaPosterIconOptions': store.toggleIcon,
                'MediaPosterOverlayOptions': store.toggleOverlay
                // Add more mappings if needed
            };


            console.log('COMPONENT NAMES => ',item.component.name)
            const toggleFunc = mappings[item.component.name];
            console.log('TOGGLE VALUE',toggleFunc);

            if (toggleFunc) {
                console.log(`updating ${item.component.name} options`, item.enabled);
                toggleFunc(item.enabled);
            }
        }

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
