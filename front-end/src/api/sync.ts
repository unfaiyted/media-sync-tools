
// Sync Options API methods
import {SyncOptions} from "@/models";
import {apiClient} from "@/api/index";

export const createSyncOption = async (option: SyncOptions): Promise<SyncOptions> => {
    const response = await apiClient.post('/sync/options/', option);
    return response.data;
}

export const fetchSyncOptions = async (optionId: string): Promise<SyncOptions> => {
    const response = await apiClient.get(`/sync/options/${optionId}`);
    return response.data;
};

export const fetchSyncOptionsByConfigId = async (configId: string): Promise<SyncOptions> => {
    const response = await apiClient.get(`/sync/options/config/${configId}`);
    return response.data;

}

export const updateSyncOption = async (option: SyncOptions): Promise<SyncOptions> => {
    const response = await apiClient.put(`/sync/options/${option.syncOptionsId}`, option);
    return response.data;
};

export const deleteSyncOption = async (optionId: string): Promise<void> => {
    await apiClient.delete(`/sync/options/${optionId}`);
}

export const triggerSyncOption = async (key :string ): Promise<SyncOptions> => {
    const response = await apiClient.get(`/sync/${key}`, { timeout:0});
    return response.data;
}
