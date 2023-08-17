import {Config, ConfigClient, Library, LibraryClient, User} from "@/models";
import {apiClient} from "@/api/index";

export const createLibrary = async (library: Library) : Promise<Library> => {
    try {
        const response = await apiClient.post('/library/', library);
        return response.data;
    } catch (error) {
        throw new Error('Error creating library');
    }
};

export const fetchLibraries = async (): Promise<Array<Library>> => {
    try {
        const response = await apiClient.get('/library/all');
        return response.data;
    } catch (error) {
        throw new Error('Error fetching libraries');
    }
};

export const deleteLibrary = async (libraryId: string | undefined) => {
    if(!libraryId) {
        console.error("Library ID is blank");
        return;
    }
    try {
        await apiClient.delete(`/library/${libraryId}`);
    } catch (error) {
        throw new Error('Error deleting library');
    }
};

export const createLibraryClient = async (libraryClient: LibraryClient): Promise<LibraryClient> => {
    try {
        const response = await apiClient.post('/library/client/', libraryClient);
        return response.data;
    } catch (error) {
        throw new Error('Error creating library client');
    }
};

export const fetchLibraryClients = async (libraryId: string): Promise<Array<LibraryClient>> => {
    try {
        const response = await apiClient.get(`/library/clients/${libraryId}`);
        return response.data;
    } catch (error) {
        throw new Error('Error fetching library clients');
    }
};

export const deleteLibraryClient = async (libraryClientId: string|undefined) => {
    if(!libraryClientId) {
        console.error("Library Client ID is blank");
        return;
    }
    try {
        await apiClient.delete(`/library/client/${libraryClientId}`);
    } catch (error) {
        throw new Error('Error deleting library client');
    }
};
