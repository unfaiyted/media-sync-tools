<template>
    <div v-if="visible" ref="menuElement"
         class="fixed z-50  bg-white rounded shadow-lg"
         :style="{ top: y + 'px', left: x + 'px' }">
        <ul>
            <li v-for="(row, index) in items"
                :key="index"
                class="p-2 hover:bg-gray-200 cursor-pointer">

                <!-- Divider -->
                <template v-if="isDivider(row)">
                    <div class="border-t my-1"></div>
                </template>

                <!-- Split Menu -->
                <template v-if="isSplit(row)">
                    <div class="flex justify-between w-full">
                        <div v-for="(item, idx) in row"
                             :key="idx"
                             class="flex items-center cursor-pointer hover:underline"
                             @click="item.action">
                            <component v-if="item.icon" :is="item.icon" class="h-5 w-5 mr-2"/>
                            {{ item.label }}
                        </div>
                    </div>
                </template>

                <!-- Regular Menu -->
                <template v-else-if="isSingleMenuItem(row)">
                    <div @click="row.action" class="flex items-center cursor-pointer hover:underline">
                        <component v-if="row.icon" :is="row.icon" class="h-5 w-5 mr-2"/>
                        {{ row.label }}
                    </div>
                </template>
            </li>
        </ul>
    </div>
</template>


<script lang="ts">
import { defineComponent, ref, watch, onMounted, onBeforeUnmount } from 'vue';
import {DividerItem, MenuItem, MenuRow} from "@/models/menu";


export default defineComponent({
    props: {
        event: Object,
        items: Array
    },
    setup(props) {
        const x = ref(0);
        const y = ref(0);
        const visible = ref(false);
        const menuElement = ref<HTMLElement | null>(null); // Add this ref for menu element

        // ... other code ...

        function isOutsideMenuThreshold(event: MouseEvent, threshold = 25) {
            const rect = menuElement.value?.getBoundingClientRect();
            if (rect) {
                const isOutsideHorizontal = event.clientX < rect.left - threshold || event.clientX > rect.right + threshold;
                const isOutsideVertical = event.clientY < rect.top - threshold || event.clientY > rect.bottom + threshold;
                return isOutsideHorizontal || isOutsideVertical;
            }
            return false;
        }

        function handleMouseMove(event: MouseEvent) {
            if (isOutsideMenuThreshold(event)) {
                closeMenu();
            }
        }

        watch(() => props.event, async (newEvent) => {
            if (newEvent) {
                console.log('EVENT!!!!!',newEvent)
                x.value = newEvent.clientX;
                y.value = newEvent.clientY;
                visible.value = true;
                // Wait for the next DOM update cycle
                await nextTick();
                document.addEventListener('mousemove', handleMouseMove);
            } else {
                document.removeEventListener('mousemove', handleMouseMove);
            }
        });


        function closeMenu() {
            visible.value = false;
        }

        function handleItemClick(item: any) {
            if (item.action) {
                item.action();
                closeMenu();
            }
            if (!item.subMenu) {
                closeMenu();
            }
        }

        const isDivider = (item: MenuRow): item is DividerItem => {
            return (item as DividerItem).type === 'divider';
        };

        const isSplit = (item: MenuRow): item is MenuItem[] => {
            return Array.isArray(item);
        };

        const isSingleMenuItem = (item: MenuRow): item is MenuItem => {
            return !isDivider(item) && !isSplit(item);
        };

        function calculateDistance(x1: number, y1: number, x2: number, y2: number) {
            const dx = x1 - x2;
            const dy = y1 - y2;
            return Math.sqrt(dx * dx + dy * dy);
        }

        onMounted(() => {
            document.addEventListener('click', closeMenu);
            document.addEventListener('mousemove', handleMouseMove);
        });

        onBeforeUnmount(() => {
            document.removeEventListener('click', closeMenu);
            document.removeEventListener('mousemove', handleMouseMove);
        });

        return {
            x,
            y,
            visible,
            isDivider,
            isSplit,
            isSingleMenuItem,
            menuElement,
            handleItemClick
        };
    }
});
</script>
