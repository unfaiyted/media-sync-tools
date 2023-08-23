<template>
  <div>
    <div v-for="(item, index) in items" :key="index" class="accordion-section mb-4 border border-gray-300 rounded-md overflow-hidden shadow">
      <button @click="toggle(index)" class="accordion-header w-full text-left bg-gray-800 text-white p-4 font-semibold hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">

        <div class="flex justify-between">

          <div>
         {{ item.title }}
          </div>

          <div>
        <VToggle v-model="item.enabled" />
          </div>

        </div>

      </button>
      <div v-if="openIndex === index" class="accordion-content bg-gray-100 p-4">
        <component :is="item.component" v-bind="item.props" />
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref } from 'vue';
import VToggle from "@/components/ui/inputs/Toggle.vue";

export default defineComponent({
  name: 'VAccordion',
  components: {VToggle},

  props: {
    items: {
      type: Array,
      required: true
    },
    autoCollapse: {
      type: Boolean,
      default: true
    }
  },

  setup(props) {
    const openIndex = ref(-1); // By default, no item is open

    const toggle = (index: number) => {
      if (props.autoCollapse) {
        openIndex.value = openIndex.value === index ? -1 : index;
      } else {
        openIndex.value = index;
      }
    };

    return {
      openIndex,
      toggle
    };
  }
});
</script>

<style scoped>
/* Add your styles here */
</style>
