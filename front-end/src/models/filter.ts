
export enum FilterType {
    UNKNOWN = 'UNKNOWN',
    TEXT = 'TEXT',
    NUMBER = 'NUMBER',
    BOOLEAN = 'BOOLEAN',
    DATE = 'DATE',
    // ... other types ...
}

export interface Filter {
    filterId?: string;
    mediaListId: string;
    filterTypeId: string;
    value: string;
}

export interface FilterTypes {
    filterTypeId: string;
    clientId: string;
    label: string;
    name: string;
    type: FilterType;
}

