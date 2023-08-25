import axios from "axios";
import { MediaList, MediaListOptions, MediaListItem } from "@/models";
import { generateGuid } from "@/utils/numbers";
import { apiClient } from "@/api/index";

// MediaList API methods
export const createMediaList = async (mediaList: MediaList) => {
    if (!mediaList.mediaListId) {
        mediaList.mediaListId = generateGuid();
    }

    return await apiClient.post('/list/', mediaList);
}

export const fetchMediaList = async (listId: string) => {
    return (await apiClient.get(`/list/${listId}`)).data;
}

// fetch media list with all items
export const fetchMediaListWithItems = async (listId: string, skip = 0, limit = 10) => {
    // Fetching the list items with skip and limit
    const media_list = (await apiClient.get(`/list/items/${listId}?skip=${skip}&limit=${limit}`)).data;
    return media_list;
}
export const fetchAllMediaLists = async () => {
    return (await apiClient.get('/list/')).data;
}

export const updateMediaList = async (updatedMediaList: MediaList) => {
    return await apiClient.put(`/list/${updatedMediaList.mediaListId}`, updatedMediaList);
}

export const deleteMediaList = async (listId: string) => {
    return await apiClient.delete(`/list/${listId}`);
}

export const fetchMediaListsForUser = async (userId: string) => {
    return (await apiClient.get(`/list/user/${userId}`)).data;
}

// MediaListOptions API methods
export const createMediaListOptions = async (listOptions: MediaListOptions) => {
    return await apiClient.post('/list/options/', listOptions);
}

export const fetchMediaListOptions = async (listOptionId: string) => {
    return (await apiClient.get(`/list/options/${listOptionId}`)).data;
}

export const updateMediaListOptions = async (updatedListOptions: MediaListOptions) => {
    return await apiClient.put(`/list/options/${updatedListOptions.mediaListOptionsId}`, updatedListOptions);
}

export const deleteMediaListOptions = async (listOptionId: string) => {
    return await apiClient.delete(`/list/options/${listOptionId}`);
}

// MediaListItem API methods
export const createMediaListItem = async (listItem: MediaListItem) => {
    return await apiClient.post('/list/item/', listItem);
}

export const fetchMediaListItem = async (itemId: string) => {
    return (await apiClient.get(`/list/item/${itemId}`)).data;
}

export const updateMediaListItem = async (updatedListItem: MediaListItem) => {
    return await apiClient.put(`/list/item/${updatedListItem.mediaItemId}`, updatedListItem);
}

export const deleteMediaListItem = async (itemId: string | undefined) => {
    if(!itemId) throw new Error("itemId is required");
    return await apiClient.delete(`/list/item/${itemId}`);
}
