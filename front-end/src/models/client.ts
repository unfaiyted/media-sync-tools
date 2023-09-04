import {FieldType, LibraryClient, ConfigClient} from "@/models";

export enum ClientType {
    UNKNOWN = 'UNKNOWN',
    MEDIA_SERVER = 'MEDIA_SERVER',
    LIST_PROVIDER = 'LIST_PROVIDER',
    ACQUISITION = 'ACQUISITION',
    UTILITY = 'UTILITY'

    // ... other types ...
}

export interface ClientField {
    clientFieldId?: string;
    clientId: string;
    name: string;
    placeholderValue?: string;
    type: FieldType;
}

export interface Client {
    clientId: string;
    label: string;
    type: ClientType;
    name: string;
    LibraryClients?: LibraryClient[];
    ConfigClient?: ConfigClient[];
}

