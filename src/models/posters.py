from enum import Enum
from typing import Optional, Tuple, List

from pydantic import BaseModel


class MediaPosterBorderOptions(BaseModel):
    enabled: bool = False
    width: int = 4
    height: int = 4
    color: Optional[Tuple[int, int, int]] = None


class MediaPosterGradientOptions(BaseModel):
    enabled: bool = False
    colors: Optional[List[Tuple[int, int, int]]] = None
    opacity: float = 0.5
    type: str = 'linear'
    angle: int = -160


class MediaPosterShadowOptions(BaseModel):
    enabled: bool = False
    color: Optional[Tuple[int, int, int]] = None
    offset: int = 5
    blur: int = 3
    transparency: int = 100


class MediaPosterTextOptions(BaseModel):
    enabled: bool = False
    text: Optional[str] = None
    font: Optional[str] = None
    position: Tuple[int, int] = (0, 0)
    color: Optional[Tuple[int, int, int]] = None
    border: Optional[MediaPosterBorderOptions] = None
    shadow: Optional[MediaPosterShadowOptions] = None


class MediaPosterBackgroundOptions(BaseModel):
    enabled: bool = False
    url: Optional[str] = None
    # image: Optional[Image] = None
    color: Optional[Tuple[int, int, int]] = None
    position: Optional[Tuple[int, int]] = (0, 0)
    opacity: float = 1.0
    border: Optional[MediaPosterBorderOptions] = None
    shadow: Optional[MediaPosterShadowOptions] = None


class IconPosition(str, Enum):
    LEFT = 'LEFT',
    MIDDLE = 'MIDDLE',
    RIGHT = 'RIGHT',
    TOP = 'TOP',
    BOTTOM = 'BOTTOM'


class MediaPosterIconOptions(BaseModel):
    enabled: bool = False
    path: Optional[str] = None
    position: IconPosition = IconPosition.TOP
    size: Tuple[int, int] = (100, 100)


class MediaPosterOverlayOptions(BaseModel):
    enabled: bool = False
    text: Optional[str] = None
    icon: Optional[MediaPosterIconOptions] = None
    position: str = 'bottom-left'
    textColor: Optional[Tuple[int, int, int]] = (255, 255, 255)
    backgroundColor: Optional[Tuple[int, int, int]] = (100, 100, 100)
    transparency: int = 100
    cornerRadius: int = 5
    border: Optional[MediaPosterBorderOptions] = None
    shadow: Optional[MediaPosterShadowOptions] = None


class MediaImageType(str, Enum):
    UNKNOWN = 'UNKNOWN'
    POSTER = 'POSTER'
    BACKGROUND = 'BACKGROUND'
    BANNER = 'BANNER'
    LOGO = 'LOGO'
    THUMB = 'THUMB'
    CLEARART = 'CLEARART'
    DISCART = 'DISCART'


class MediaPoster(BaseModel):
    mediaPosterId: Optional[str] = None
    mediaItemId: Optional[str] = None
    url: Optional[str] = None
    width: int
    height: int
    type: MediaImageType
    border: Optional[MediaPosterBorderOptions]
    text: Optional[MediaPosterTextOptions]
    gradient: Optional[MediaPosterGradientOptions]
    background: Optional[MediaPosterBackgroundOptions]
    overlays: Optional[List[MediaPosterOverlayOptions]]
    icon: Optional[MediaPosterIconOptions]
    mediaItem: Optional[str]


class ProviderPoster(BaseModel):
    providerPosterId: Optional[str] = None
    providerId: str
    url: str
    width: int
    height: int
    type: MediaImageType
