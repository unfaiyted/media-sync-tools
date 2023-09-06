<template>
    <div v-if="isHydrated">
      <SettingsTabs/>
    </div>
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
import SettingsTabs from "@/components/settings/SettingsTabs.vue";
export default defineComponent({
  computed: {
    ClientType() {
      return ClientType
    }
  },
    components: {
      SettingsTabs,
        ClientFieldManagement,
        UserManagement,
        ListEditor,
      ClientButtonGroup,
        ClientManager,
        SyncOptions,
    },
    data() {
        return {
            config: Object as unknown as Config,
            isHydrated: false,
        }
    },
    async mounted() {
      const store = useAppConfigStore();
        this.config = await store.getAppConfig('APP-DEFAULT-USER');
        this.isHydrated = true;


        // Watching for changes in config
        watch(() => this.config, (newValue, oldValue) => {
            if (newValue !== oldValue) {
                // Handle the change here
                console.log('changes')
                // Update the template or perform any other side effect
            }
        });

    },
    setup() {


        return {
            ClientType
        }
    },
    methods: {}
});
</script>


<style scoped>
/* Add your custom styles here if needed */
</style>
