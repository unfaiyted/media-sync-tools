// src/stores/listStore.ts

import { defineStore } from 'pinia';
import {
    MediaList, MediaListOptions, MediaListItem
} from "@/models";
import {
    createMediaList, fetchMediaList, fetchMediaListWithItems,
    fetchAllMediaLists, updateMediaList, deleteMediaList,
    fetchMediaListsForUser, createMediaListOptions,
    fetchMediaListOptions, updateMediaListOptions, deleteMediaListOptions,
    createMediaListItem, fetchMediaListItem, updateMediaListItem, deleteMediaListItem
} from "@/api/lists";
import {requestPosterForItem} from "@/api/posters";

interface ListState {
    mediaLists: MediaList[];
    mediaListOptions: MediaListOptions[];
    loading: boolean;
    error: boolean;
    errorMessage: string;
}

export const useListStore = defineStore({
    id: 'mediaList',
    state(): ListState {
        return {
            mediaLists: [],
            mediaListOptions: [],
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

        asyncWrapper: async function(action: (...args: any[]) => Promise<any>, ...args: any[]) {
            try {
                return await action(...args);
            } catch (err) {
                this.handleError(err);
            } finally {
                if (!this.error) this.loading = false;
            }
        },

        fetchAllLists: async function(): Promise<MediaList[]> {
            this.mediaLists = await this.asyncWrapper(fetchAllMediaLists);
            return this.mediaLists;
        },

        fetchUserLists: async function(userId: string): Promise<MediaList[]> {
            this.mediaLists = await this.asyncWrapper(fetchMediaListsForUser, userId);
            return this.mediaLists;
        },
        fetchListWithItems: async function(listId: string | string[]) {
            // todo: handle multiple listIds
            const mediaList = await this.asyncWrapper(fetchMediaListWithItems, listId);
            if (mediaList) {
                const index = this.mediaLists.findIndex(list => list.mediaListId === mediaList.mediaListId);
                if (index >= 0) {
                    this.mediaLists[index] = mediaList;
                } else {
                    this.mediaLists.push(mediaList);
                }
            }
            return mediaList;
        },

        getListWithItems: async function(listId: string | string[]) {
            const index = this.mediaLists.findIndex(list => list.mediaListId === listId);
            const list = (index >= 0) ? this.mediaLists[index] : null;


            console.log(list)
            if(list && list.items && list.items.length > 0) {
                return list;
            }

            console.log('Fetching list with items');
            return await this.fetchListWithItems(listId);
        },
        addList: async function(mediaList: MediaList) {
            const newList = await this.asyncWrapper(createMediaList, mediaList);
            if (newList) this.mediaLists.push(newList);
        },

        updateList: async function(updatedMediaList: MediaList) {
            const updatedList = await this.asyncWrapper(updateMediaList, updatedMediaList);
            const index = this.mediaLists.findIndex(list => list.mediaListId === updatedList.mediaListId);
            if (index >= 0) this.mediaLists[index] = updatedList;
        },

        removeList: async function(listId: string) : Promise<MediaList[]> {
            this.asyncWrapper(deleteMediaList, listId);
            const index = this.mediaLists.findIndex(list => list.mediaListId === listId);
            if (index >= 0) this.mediaLists.splice(index, 1);
            return this.mediaLists;
        },

        addListItem: async function(listItem: MediaListItem) {
            const newItem = await this.asyncWrapper(createMediaListItem, listItem);
            // if (newItem) this./*mediaListItems*/.push(newItem);
        },

        updateListItem: async function(updatedListItem: MediaListItem) {
            const updatedItem = await this.asyncWrapper(updateMediaListItem, updatedListItem);
            // const index = this.mediaListItems.findIndex(item => item.mediaItemId === updatedItem.mediaItemId);
            // if (index >= 0) this.mediaListItems[index] = updatedItem;
        },

        removeListItem: async function(listId: string, itemId: string) {
            await this.asyncWrapper(deleteMediaListItem, itemId);

            const list = this.mediaLists.find(list => list.mediaListId === listId);

            if (list) {
                const index = list.items?.findIndex(item => item.mediaItemId === itemId) || -1;
                if (index >= 0) list.items?.splice(index, 1);
            }

            return this.getListWithItems(listId);
        },

        updateListItemPoster: async function(itemId: string) {
            const updatedItem = await this.asyncWrapper(requestPosterForItem, itemId);
            const list = this.mediaLists.find(list => list.mediaListId === updatedItem.mediaListId);
            if (list) {
                const index = list.items?.findIndex(item => item.mediaItemId === updatedItem.mediaItemId) || -1;
                if (index >= 0) list.items?.splice(index, 1, updatedItem);

            }

            return this.getListWithItems(updatedItem.mediaListId);
        },
        resetState() {
            this.mediaLists = [];
            this.mediaListOptions = [];
            this.loading = true;
            this.error = false;
            this.errorMessage = '';
        }
    }
});
