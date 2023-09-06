<template>
    <Modal :isOpen="isOpen"
           @do-action="saveProviderChanges"
           do-action-text="Save Changes"
           cancel-action-text="Cancel"
           @cancel-action="cancelAction">
        <div class="p-4">
            <h3 class="text-xl mb-4 text-white">Edit Provider: {{ provider?.client?.name }}</h3>

            <div v-if="provider?.client">
                <!-- Edit Client Fields -->
                <div v-for="field in mergedFields" :key="field.clientFieldId">
                    <label class="block mb-2 text-white">{{ field.name }}:</label>
                    <input v-model="field.value" :type="field.type === 'PASSWORD' ? 'password' : 'text'" class="border p-2 rounded w-full mb-4" :placeholder="field.placeholderValue" />
                </div>

            </div>
        </div>
    </Modal>
</template>


<script lang="ts">
import Modal from "@/components/ui/Modal.vue";
import {ClientType, ConfigClient} from "@/models";
import {onMounted, PropType, ref} from "vue";

export default defineComponent({
    name: 'SettingsProviderModal',
    components: {Modal},
    props: {
        provider: {
            type: Object as PropType<ConfigClient>,
            required: true,
        },

    },
    setup(props, {emit}) {
        const isOpen = ref(false);
        // const config = useAppConfigStore();
        const mergedFields = computed(() => {
            return props.provider.clientFields.map(field => {
                const fieldValue = props.provider.clientFieldValues.find(fv => fv.configClientFieldId === field.clientFieldId);
                return {
                    ...field,
                    value: fieldValue ? fieldValue.value : ''
                };
            });
        });

        const cancelAction = () => {
            console.log('cancelAction');
            emit('close', false);
        };


        const saveProviderChanges = () => {
            // config.saveProvider(selectedProvider.value);
            isOpen.value = false;
        };

        onMounted(() => {
            // config.logcadProviders();
        });

        return {
            isOpen,
            saveProviderChanges,
            // config,
            mergedFields,
            cancelAction,
        };
    }
});
</script>
