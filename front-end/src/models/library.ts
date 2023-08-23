export enum LibraryType {
    UNKNOWN = 'UNKNOWN',
    MOVIES = 'MOVIES',
    SHOWS = 'SHOWS',
    MUSIC = 'MUSIC',
    BOOKS = 'BOOKS',
    GAMES = 'GAMES',
    AUDIOBOOKS = 'AUDIOBOOKS',
    ANIME = 'ANIME',

}


export interface Library {
    libraryId?: string;
    configId: string;
    name: string;
    type: LibraryType;
    clients?: LibraryClient[];
    List?: MediaList;
}

export interface LibraryClient {
    libraryClientId?: string;
    libraryId: string;
    libraryName: string;
    client?: Client;
    clientId: string;
    mediaListId?: string;
    Library?: Library;
}

