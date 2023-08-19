<template>
    <!--        <ClientManager />-->

    <!--    <UserManagement />-->
    <div v-if="config">
<!--        <ClientsConfig :config="config" />
        <LibraryManager :config="config"  />-->
    </div>
  <ClientButtonGroup :type="ClientType.MEDIA_SERVER" />
  <ClientButtonGroup :type="ClientType.UTILITY" />

    <!--    <ListEditor />-->
</template>

<script lang="ts">
import ClientFieldManagement from "@/components/admin/ClientFieldManagement.vue";
import ClientManager from "@/components/admin/ClientManager.vue";
import ClientsConfig from "@/components/config/ClientsConfig.vue";
import UserManagement from "@/components/admin/UserManager.vue";
import ClientButtonGroup from "@/components/ui/ClientButtonGroup.vue";
import LibraryManager from "@/components/config/LibraryManager.vue";
import ListEditor from "@/components/ListEditor.vue";
import SyncOptions from "@/components/config/SyncOptions.vue";
import {ClientType, Config} from "@/models";
import {fetchConfig} from "@/api/configs";
export default defineComponent({
  computed: {
    ClientType() {
      return ClientType
    }
  },
    components: {
        ClientFieldManagement,
        ClientsConfig,
        UserManagement,
        ListEditor,
      ClientButtonGroup,
        ClientManager,
        SyncOptions,
        LibraryManager
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
        this.config = await fetchConfig(this.configId);
        console.log(this.config);
    },
    methods: {}
});
</script>


<style scoped>
/* Add your custom styles here if needed */
</style>
