// ... other imports
import axios from "axios";
import {Config, ConfigClient} from "@/models";
import { generateGuid } from "@/utils/numbers";
import {apiClient} from "@/api/index";

export const createConfig = async (config: Config) => {
    if (!config.configId) {
        config.configId = generateGuid();
    }

    return await apiClient.post('/config/', config);
}

export const fetchConfig = async (configId: string) => {
    return (await apiClient.get(`/config/${configId}`)).data;
}

export const fetchConfigByUserId= async (userId: string | undefined) => {
    if(!userId) {
        console.error("Config ID is blank");
        return;
    }
    return await apiClient.get(`/config/?userId=${userId}`);
}

export const updateConfig= async (updatedConfigClient: ConfigClient) => {
    return await apiClient.put(`/config/${updatedConfigClient.configClientId}`, updatedConfigClient);
}

export const deleteConfig = async (configClientId: string | undefined) => {
    if(!configClientId) {
        console.error("Config ID is blank");
        return;
    }
    return await apiClient.delete(`/config/${configClientId}`);
}

// ConfigClient API methods
export const createConfigClient = async (configClient: ConfigClient) => {
        configClient.configClientId = generateGuid();
    return await apiClient.post('/config/client/', configClient);
}

export const fetchConfigClient = async (configClientId: string) => {
    return await apiClient.get(`/config/client/${configClientId}`);
}

export const fetchConfigClientByConfigId = async (configId: string | undefined) => {
    if(!configId) {
        console.error("Config ID is blank");
        return;
    }
    return (await apiClient.get(`/config/client/?configId=${configId}`)).data;
}

export const updateConfigClient = async (updatedConfigClient: ConfigClient) => {
    return await apiClient.put(`/config/client/${updatedConfigClient.configClientId}`, updatedConfigClient);
}

export const deleteConfigClient = async (configClientId: string | undefined) => {
    if(!configClientId) {
        console.error("Config ID is blank");
        return;
    }
    return await apiClient.delete(`/config/client/${configClientId}`);
}
