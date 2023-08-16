<template>
<!--        <ClientCreator />-->

<!--    <UserManagement />-->
    <div v-if="config">
        <ClientsConfig :config="config" />
    </div>
</template>

<script lang="ts">
import ClientFieldManagement from "@/components/admin/ClientFieldManagement.vue";
import ClientCreator from "@/components/admin/ClientManager.vue";
import ClientsConfig from "@/components/config/ClientsConfig.vue";
import UserManagement from "@/components/admin/UserManager.vue";
import {Config} from "@/models";
import {fetchConfig} from "@/api/configs";
export default defineComponent({
    components: {
        ClientFieldManagement,
        ClientsConfig,
        UserManagement,
        ClientCreator
    },
    data() {
        return {
            config: {
                configId: '4158646e-631e-462b-bf07-5b39cf2cc3ae'
            } as Config,
            configId: '4158646e-631e-462b-bf07-5b39cf2cc3ae'
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
