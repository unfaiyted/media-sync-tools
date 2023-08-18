<template>
  <div v-if="visible"
       class="fixed z-50 bg-white rounded shadow-lg"
       :style="{ top: y + 'px', left: x + 'px' }">
    <ul>
      <li v-for="item in items"
          :key="item.label"
          @click="item.action"
          class="p-2 hover:bg-gray-200 cursor-pointer">
        {{ item.label }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch, onMounted, onBeforeUnmount } from 'vue';

export default defineComponent({
  props: {
    event: Object,
    items: Array
  },
  setup(props) {
    const x = ref(0);
    const y = ref(0);
    const visible = ref(false);

    watch(() => props.event, (newEvent) => {
      if (newEvent) {
        x.value = newEvent.clientX;
        y.value = newEvent.clientY;
        visible.value = true;
      }
    });

    function closeMenu() {
      visible.value = false;
    }

    onMounted(() => {
      document.addEventListener('click', closeMenu);
    });

    onBeforeUnmount(() => {
      document.removeEventListener('click', closeMenu);
    });

    return {
      x,
      y,
      visible
    };
  }
});
</script>
