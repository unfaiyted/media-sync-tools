<template>
    <div class="p-6">
        <h1 class="text-3xl font-bold mb-4">Sync Options Management</h1>
        <div class="mb-4" v-for="(optionKey, index) in booleanOptionKeys" :key="index">
            <div class="flex items-center justify-between mb-2">
                <label class="font-semibold">{{ camelCaseToWords(optionKey) }}</label>
                <label class="switch">
                    <input type="checkbox" v-model="syncOptions[optionKey]" @change="updateOption(optionKey)" class="hidden">
                    <span class="slider round"></span>
                </label>
            </div>
            <button @click="triggerOption(optionKey)" :class="triggerButtonClasses(optionKey)">
                <span v-if="isLoading[optionKey]">Loading...</span>
                <span v-else>Trigger</span>
            </button>
        </div>
    </div>
</template>

<style scoped>
.switch {
    position: relative;
    display: inline-block;
    width: 40px;
    height: 20px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: .4s;
    transition: .4s;
    border-radius: 34px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 2px;
    bottom: 2px;
    background-color: white;
    -webkit-transition: .4s;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: #2196F3;
}

input:focus + .slider {
    box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
    -webkit-transform: translateX(20px);
    -ms-transform: translateX(20px);
    transform: translateX(20px);
}
</style>

<script lang="ts">
import { ref, onMounted } from 'vue';
import {Config, SyncOptions} from '@/models';
import {fetchSyncOptionsByConfigId, triggerSyncOption, updateSyncOption} from '@/api/sync';
import {camelCaseToWords} from "@/utils/string";
export default defineComponent({
    props: {
        config: {
            type: Object as () => Config,
            required: true
        }
    },
    setup(props: { config: Config }) {
        const syncOptions = ref<SyncOptions>();
        const booleanOptionKeys = ref<string[]>([]);
        const isLoading = ref<Record<string, boolean>>({});

        const fetchOptions = async () => {
            if(props.config.configId === undefined){
                return;
            }

            try {
                const options = await fetchSyncOptionsByConfigId(props.config.configId);
                syncOptions.value = options;
                booleanOptionKeys.value = Object.keys(options).filter(key => typeof options[key] === 'boolean');
            } catch (error) {
                console.error('Error fetching sync options:', error);
            }
        };

        const triggerOption = async (optionKey: string) => {
            isLoading.value[optionKey] = true;
            try {
                console.log('Triggered option:', optionKey);
                await triggerSyncOption(optionKey);
            } finally {
                isLoading.value[optionKey] = false;
            }
        };


         const updateOption = async (optionKey: string) =>{
            if(props.config.configId === undefined || (syncOptions.value && syncOptions.value[optionKey] === undefined)){
                 return;
             }

            const options = syncOptions.value

            await updateSyncOption({
                ...options as unknown as SyncOptions,
                configId: props.config.configId,
                // @ts-ignore
                [optionKey]: syncOptions.value[optionKey]
            });
            console.log('Triggered option:', optionKey);
        };


        const triggerButtonClasses = (optionKey: string) => ({
            'px-4 py-2 bg-blue-500 text-white rounded': true,
            'opacity-50 cursor-not-allowed': isLoading.value[optionKey]
        });

        onMounted(() => {
            fetchOptions();
        });

        return {
            syncOptions,
            booleanOptionKeys,
            camelCaseToWords,
            triggerButtonClasses,
            triggerOption,
            isLoading,
            updateOption
        };
    }
})
</script>
