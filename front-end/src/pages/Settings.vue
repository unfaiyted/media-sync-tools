<template>

    <div v-if="config">
    </div>
  <ClientButtonGroup :type="ClientType.MEDIA_SERVER" />
  <ClientButtonGroup :type="ClientType.UTILITY" />

</template>

<script lang="ts">
import ClientFieldManagement from "@/components/admin/ClientFieldManagement.vue";
import ClientManager from "@/components/admin/ClientManager.vue";
import UserManagement from "@/components/admin/UserManager.vue";
import ClientButtonGroup from "@/components/ui/ClientButtonGroup.vue";
import ListEditor from "@/components/ListEditor.vue";
import SyncOptions from "@/components/config/SyncOptions.vue";
import {ClientType, Config} from "@/models";
import {fetchConfig} from "@/api/configs";
import {useAppConfigStore} from "@/store/appConfigStore";
export default defineComponent({
  computed: {
    ClientType() {
      return ClientType
    }
  },
    components: {
        ClientFieldManagement,
        UserManagement,
        ListEditor,
      ClientButtonGroup,
        ClientManager,
        SyncOptions,
    },
    data() {
        return {
            config: {
                configId: 'APP-DEFAULT-CONFIG'
            } as Config,
        }
    },
    async mounted() {
      const store = useAppConfigStore();
        this.config = await store.getAppConfig('APP-DEFAULT-CONFIG');
    },
    methods: {}
});
</script>


<style scoped>
/* Add your custom styles here if needed */
</style>
