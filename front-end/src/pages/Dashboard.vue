<template>
  <div class="p-6 bg-gray-100 min-h-screen">
    <h1 class="text-2xl font-semibold mb-4">Dashboard</h1>

    <!-- Overview section -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-white p-4 rounded shadow-lg flex items-center justify-between">
        <span>Total Movies</span>
        <span class="text-xl font-bold">1,234</span>
      </div>
      <div class="bg-white p-4 rounded shadow-lg flex items-center justify-between">
        <span>Total Shows</span>
        <span class="text-xl font-bold">567</span>
      </div>
      <div class="bg-white p-4 rounded shadow-lg flex items-center justify-between">
        <span>Server Status</span>
        <span class="text-green-500">Online</span>
      </div>
    </div>

    <!-- Recently Added section -->
    <div class="bg-white p-4 rounded shadow-lg">
      <h2 class="text-lg font-semibold mb-4">Recently Added Movies</h2>
      <!-- Movie list, potentially a component iterating over the recent movies -->
    </div>

      <MediaListUrlImporter/>

      <SyncOptions :config="config"/>


  </div>
</template>
<script  lang="ts">
import SyncOptions from "@/components/config/SyncOptions.vue";
import {Config} from "@/models";
import {fetchConfig} from "@/api/configs";
import {useAppConfigStore} from "@/store/appConfigStore";


export default defineComponent({
    components: {
        SyncOptions
    },
    data() {
        return {
            config: {
                configId: 'APP-DEFAULT-CONFIG'
            } as Config,
            configId: 'APP-DEFAULT-CONFIG'
        }
    },
    async mounted() {
      const store = useAppConfigStore();
        // this.config = await store.getAppConfig('APP-DEFAULT-CONFIG')
        console.log(this.config);
    },
    methods: {}
});


</script>
