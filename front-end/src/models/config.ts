import {ClientField, Library, User, Client} from "@/models/index";

export enum FieldType {
    STRING = 'STRING',
    BOOLEAN = 'BOOLEAN',
    NUMBER = 'NUMBER',
    PASSWORD = 'PASSWORD'

}

export interface ConfigClient {
    configClientId?: string;
    label: string;
    client: Client;
    clientId: string;
    relatedConfig: Config;
    configId: string;
    clientFields: ConfigClientFieldsValue[];
}

export interface ConfigClientFieldsValue {
    configClientFieldValueId?: string; // This is the ID of the value, not the field
    configClientFieldId?: string; // This is the ID of the field, not the value (ClientField)
    clientField?: ClientField; // This is the field object
    configClientId: string; // This is the ID of the client config (ConfigClient)
    value: string; // This is the value of the field
}



export interface Config {
    configId?: string;
    user: User;
    userId: string;
    clients?: ConfigClient[];
    libraries?: Library[];
    sync?: SyncOptions;
}

export interface SyncOptions {
    syncOptionsId?: string;
    configId: string;
    collections: boolean;
    playlists: boolean;
    lovedTracks: boolean;
    topLists: boolean;
    watched: boolean;
    ratings: boolean;
    libraries: boolean;
    trakt: boolean;
    relatedConfig?: Config;
}
