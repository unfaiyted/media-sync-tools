// src/stores/appConfigStore.js

import { defineStore } from 'pinia';
import {ClientType, Config, ConfigClient} from "@/models";
import {
    deleteConfigClient, fetchClientFieldValuesByClientId, fetchConfigClient,
    fetchConfigClientsByConfigId,
    fetchConfigClientsByType, fetchFieldsValueByConfigId,
    hydrateApp as hydrateAPI,
    updateConfig as updateAPI, updateConfigClient
} from "@/api/configs";
import {fetchLibraries} from "@/api/libraries";

interface AppState {
    appConfig: Config | null;
    loading: boolean;
    error: boolean;
    errorMessage: string;
}

export const useAppConfigStore = defineStore({
    id: 'appConfig',
    state(): AppState {
        return {
            appConfig: null,
            loading: true,
            error: false,
            errorMessage: '',
        };
    },
    actions: {
        handleError(err: any) {
            this.error = true;
            this.errorMessage = err.response ? err.response.data.detail : 'An unexpected error occurred';
            this.loading = false;
        },

        asyncWrapper: async function (action: (...args: any[]) => Promise<any>, ...args: any[]) {
            try {
                return await action(...args);
            } catch (err) {
                this.handleError(err);
            } finally {
                if (!this.error) this.loading = false;
            }
        },

        hydrateApp: async function (userId: string) {
            this.appConfig = await this.asyncWrapper(hydrateAPI, userId);
            console.log('hydrated', this.appConfig);
        },
        getAppConfig: async function (userId: string) {
            return (this.appConfig) ? this.appConfig : this.appConfig = await this.asyncWrapper(hydrateAPI, userId);
        },
        getConfigClient: async function (configClient: ConfigClient) {
            if (this.appConfig) {
                return (this.appConfig.clients) ? this.appConfig.clients : this.appConfig.clients = await this.asyncWrapper(fetchConfigClient, configClient);
            }
        },
        getConfigClientByType: async function (configId: string, type: string) {
            if(this.appConfig?.clients) {
                // Filter and return by type
               return this.appConfig.clients.filter((configClient : ConfigClient) => configClient.configId === configId && configClient.client.type === type);
            }
        },
        getConfigClientsByConfigId: async function (configId: string) {
            if(this.appConfig?.clients) {
                // Filter and return by type
                return this.appConfig.clients.filter((configClient : ConfigClient) => configClient.configId === configId);
            }
        },
        getClientFieldValuesByClientId: async function (clientId: string) {
           if(this.appConfig?.clients) {
            return this.appConfig.clients.filter((configClient : ConfigClient) => configClient.client.clientId === clientId);
           }
        },
        getClientFieldValuesByConfigId: async function (configId: string) {
            if(this.appConfig?.clients) {
                return this.appConfig.clients.filter((configClient : ConfigClient) => configClient.configId === configId);
            }
        },
        getLibraries: async function () {
            if(this.appConfig?.libraries) {
                return this.appConfig.libraries
            }
            // fetch libraries
            console.log("Fetching libraries");
            this.appConfig.libraries = await this.asyncWrapper(fetchLibraries);
            return this.appConfig.libraries;
        },
        updateConfigClient: async function (configClient: ConfigClient) {
            // Update the config client in the appConfig
            if(this.appConfig?.clients) {
                const index = this.appConfig.clients.findIndex((configClient : ConfigClient) => configClient.configClientId === configClient.configClientId);
                this.appConfig.clients[index] = configClient;
            }
            return await updateConfigClient(configClient)
        },
        deleteConfigClient: async function (configClientId: string) {
            if(this.appConfig?.clients) {
                const index = this.appConfig.clients.findIndex((configClient : ConfigClient) => configClient.configClientId === configClientId);
                this.appConfig.clients.splice(index, 1);
            }
            return await deleteConfigClient(configClientId);
        },
        resetState() {
            this.appConfig = null;
            this.loading = true;
            this.error = false;
            this.errorMessage = '';
        }
    },

});
