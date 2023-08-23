import axios from "axios";
import {MediaList, MediaListOptions, MediaListItem, MediaPoster} from "@/models";
import { generateGuid } from "@/utils/numbers";
import { apiClient } from "@/api/index";

// Poster calls

export const fetchPoster = async (mediaItemId: string) => {
    return (await apiClient.get(`/poster/${mediaItemId}`)).data;
}

export const requestPosterForItem = async (mediaItemId: string): Promise<MediaListItem> => {
    return (await apiClient.get(`/poster/item/${mediaItemId}`)).data;
}

export const updateMediaPoster = async (mediaPoster: MediaPoster) => {
    return (await apiClient.put(`/poster/${mediaPoster.mediaItemId}`, mediaPoster)).data;
}
export const createMediaPoster = async (mediaPoster: MediaPoster) => {
    console.log('POSTERERRR',mediaPoster);
    return  await apiClient.post(`/poster`, mediaPoster, {responseType:"blob"});
}
export const deleteMediaPoster = async (mediaPosterId: string) => {
    return (await apiClient.delete(`/poster/${mediaPosterId}`)).data;
}

export const requestPostersForList = async (mediaListId: string) => {
    return (await apiClient.get(`/poster/list/${mediaListId}`)).data;
}

export const fetchIconFilenames = async () => {
    return (await apiClient.get('/poster/icons/')).data.filenames;
}

export const fetchBackgroundImageFilenames = async () => {
    return (await apiClient.get('/poster/backgrounds/')).data.filenames;
}


// Files
// Get Icons
export const fetchIcons = async () => {
    return (await apiClient.get('/poster/icons/')).data;
}

export const fetchBackgroundImages = async (): Promise<FileList> => {
    return (await apiClient.get('/poster/backgrounds/')).data.files;
}

export const uploadPoster = async (file: File) => {
    return (await apiClient.post('/poster/upload/', file)).data;
}
