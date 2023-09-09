
// Sync Options API methods
import {MediaList, MediaListOptions, SyncOptions} from "@/models";
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


export const syncListToProviders = async (listOptions: MediaListOptions): Promise<MediaListOptions> => {
    const response = await apiClient.post(`/sync/list/`, listOptions, { timeout:0});
    return response.data;
}

// sync list to client
export const syncListToClient = async (clientId: string, listId: string): Promise<SyncOptions> => {
    const response = await apiClient.get(`/sync/list/${listId}/client/${clientId}`, { timeout:0});
    return response.data;
}

export const importMediaListFromUrl = async (url: string): Promise<MediaList> => {
    const response = await apiClient.post('/sync/import/list/', { url });
    return response.data as MediaList;
}

