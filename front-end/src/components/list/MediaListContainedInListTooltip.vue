<template>
  <Tooltip>
    <template #trigger>
      <span class="ml-2 text-blue-500 cursor-pointer">&#8226;</span> <!-- This is your dot -->
    </template>
    <!-- Tooltip Content -->
    <div v-if="containedInLists.length">
      <div v-for="list in containedInLists" :key="list.id">
        {{ list.name }}
      </div>
    </div>
  </Tooltip>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import Tooltip from '@/components/ui/inputs/Tooltip.vue';

export default defineComponent({
  components: {
    Tooltip
  },
  props: {
    containedInLists: {
      type: Array as PropType<Array<{ id: string; name: string }>>,
      required: true,
      default: () => []
    }
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
