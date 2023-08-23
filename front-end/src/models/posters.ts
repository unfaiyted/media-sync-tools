export type Color = string | [number, number, number];

export enum ListType {
    COLLECTION = "COLLECTION",
    PLAYLIST = "PLAYLIST",
    // ... other types ...
}

export enum IconPosition {
    LEFT = 'LEFT',
    MIDDLE = 'MIDDLE',
    RIGHT = 'RIGHT',
    TOP = 'TOP',
    BOTTOM = 'BOTTOM'
}


export enum MediaImageType {
    UNKNOWN = 'UNKNOWN',
    POSTER = 'POSTER',
    BACKGROUND = 'BACKGROUND',
    BANNER = 'BANNER',
    LOGO = 'LOGO',
    THUMB = 'THUMB',
    CLEARART = 'CLEARART',
    DISCART = 'DISCART',
}

export interface MediaPosterBorderOptions {
    enabled: boolean;
    width: number;
    height: number;
    color?: Color;
}

export interface MediaPosterGradientOptions {
    enabled: boolean;
    colors?: Color[];
    opacity: number;
    type: string;
    angle: number;
}

export interface MediaPosterShadowOptions {
    enabled: boolean;
    color?: Color;
    offset: number;
    blur: number;
    transparency: number;
}

export interface MediaPosterTextOptions {
    enabled: boolean;
    text?: string;
    position: [number, number];
    color?: Color;
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}

export interface MediaPosterBackgroundOptions {
    enabled: boolean;
    url?: string;
    color?: Color;
    position?: [number, number];
    size?: [number, number];
    opacity: number;
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}


export interface MediaPosterOverlayOptions {
    enabled: boolean;
    text?: string;
    position: string;
    textColor?: Color;
    backgroundColor?: Color;
    transparency: number;
    cornerRadius: number;
    icon?: MediaPosterIconOptions;
    border?: MediaPosterBorderOptions;
    shadow?: MediaPosterShadowOptions;
}

export interface MediaPoster {
    mediaPosterId?: string;
    mediaItemId?: string;
    url?: string;
    width: number;
    height: number;
    type: MediaImageType;
    border?: MediaPosterBorderOptions;
    text?: MediaPosterTextOptions;
    gradient?: MediaPosterGradientOptions;
    background?: MediaPosterBackgroundOptions;
    icon?: MediaPosterIconOptions;
    overlays?: MediaPosterOverlayOptions[];
    mediaItem?: string;
}

export interface MediaPosterIconOptions {
    enabled: boolean;
    path?: string;
    position: IconPosition;
    size: [number, number];
}




// POSTER FROM A PROVIDER
export interface ProviderPoster {
    providerPosterId?: string;
    providerId: string; // configClientID
    url: string;
    width?: number;
    height?: number;
    type: MediaImageType;

}

