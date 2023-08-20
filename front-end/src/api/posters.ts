import axios from "axios";
import { MediaList, MediaListOptions, MediaListItem } from "@/models";
import { generateGuid } from "@/utils/numbers";
import { apiClient } from "@/api/index";

// Poster calls

export const fetchPoster = async (mediaItemId: string) => {
    return (await apiClient.get(`/poster/${mediaItemId}`)).data;
}

export const requestPosterForItem = async (mediaItemId: string) => {
    return (await apiClient.get(`/poster/item/${mediaItemId}`)).data;
}

export const requestPostersForList = async (mediaListId: string) => {
    return (await apiClient.get(`/poster/list/${mediaListId}`)).data;
}

