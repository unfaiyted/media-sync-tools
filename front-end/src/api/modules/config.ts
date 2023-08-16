import request from '@/utils/axios';

interface IResponseType<P = Record<string, any>> {
    code?: number;
    status: number;
    msg: string;
    data: P;
}


type ClientType = 'plex' | 'jellyfin' | 'emby';

type Client = {
     [key: string] : {
         label: string;
         type: ClientType;
         name: string;
         [key: string]: any;
         // other fields unique to each client type
     }
}


interface Config {
    clients: Record<string, any>;
    libraries: Record<string, any>;
    sync: Record<string, any>;
    collections: Record<string, any>;
    playlists: Record<string, any>;
}

interface ClientConfig {
    server_url: string;
    access_token: string;
    type: string;
}

interface ConfigUpdate {
    userId: string;
    clientData: Record<string, any>;
}

const getConfig = () => {
    return request<IResponseType<Config>>({
        url: '/api/config/',
        method: 'get',
    });
};

const updateConfig = (data: ConfigUpdate) => {
    return request<IResponseType<Config>>({
        url: '/api/config/',
        method: 'put',
        data,
    });
};

const deleteConfig = () => {
    return request<IResponseType<{}>>({
        url: '/api/config/',
        method: 'delete',
    });
};

const createConfig = () => {
    return request<IResponseType<{}>>({
        url: '/api/config/',
        method: 'post',
    });
};

const deleteClient = (client_id: string) => {
    return request<IResponseType<{}>>({
        url: `/api/config/client/${client_id}`,
        method: 'delete',
    });
};

const updateLibrariesConfig = (data: Record<string, any>) => {
    return request<IResponseType<Config>>({
        url: '/api/config/libraries',
        method: 'put',
        data,
    });
};

const updateSyncConfig = (data: Record<string, any>) => {
    return request<IResponseType<Config>>({
        url: '/api/config/sync',
        method: 'put',
        data,
    });
};

const getLibraries = () => {
    return request<IResponseType<Record<string, any>>>({
        url: '/api/config/libraries',
        method: 'get',
    });
};

export {
    getConfig,
    updateConfig,
    deleteConfig,
    createConfig,
    deleteClient,
    updateLibrariesConfig,
    updateSyncConfig,
    getLibraries,
};
