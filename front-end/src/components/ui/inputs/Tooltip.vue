<!-- components/Tooltip.vue -->

<template>
    <div class="relative">
        <slot name="trigger"></slot>
        <div class="absolute z-10 hidden p-2 bg-black text-white rounded mt-2 tooltip-content">
            <slot></slot>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'Tooltip',
    mounted() {
        const trigger = this.$slots.trigger?.()[0].el;
        const tooltipContent = this.$el.querySelector('.tooltip-content');

        trigger.addEventListener('mouseenter', () => {
            tooltipContent.style.display = 'block';
        });

        trigger.addEventListener('mouseleave', () => {
            tooltipContent.style.display = 'none';
        });
    }
});
</script>

<style scoped>
.tooltip-content {
    min-width: 150px;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
}
</style>
