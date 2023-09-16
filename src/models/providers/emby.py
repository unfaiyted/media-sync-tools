from pydantic import BaseModel
from typing import Dict, List, Optional

from enum import Enum

from src.models import MediaItemType


class EmbyItemType(Enum):
    AUDIO = "Audio"
    VIDEO = "Video"
    FOLDER = "Folder"
    EPISODE = "Episode"
    MOVIE = "Movie"
    TRAILER = "Trailer"
    ADULT_VIDEO = "AdultVideo"
    MUSIC_VIDEO = "MusicVideo"
    BOX_SET = "BoxSet"
    MUSIC_ALBUM = "MusicAlbum"
    MUSIC_ARTIST = "MusicArtist"
    SEASON = "Season"
    SERIES = "Series"
    GAME = "Game"
    GAME_SYSTEM = "GameSystem"
    BOOK = "Book"


    @classmethod
    def from_media_type(cls, type: MediaItemType):

        if type == MediaItemType.MOVIE:
            return cls.MOVIE
        elif type == MediaItemType.SHOW:
            return cls.SERIES
        elif type == MediaItemType.SEASON:
            return cls.SEASON
        elif type == MediaItemType.EPISODE:
            return cls.EPISODE
        elif type == MediaItemType.LIST:
            return cls.BOX_SET

        return cls.FOLDER




class EmbyImageType(Enum):
    PRIMARY = "Primary"
    ART = "Art"
    BACKDROP = "Backdrop"
    BANNER = "Banner"
    LOGO = "Logo"
    THUMB = "Thumb"
    DISC = "Disc"
    BOX = "Box"
    SCREENSHOT = "Screenshot"
    MENU = "Menu"
    CHAPTER = "Chapter"


class EmbyUserData(BaseModel):
    PlaybackPositionTicks: int
    PlayCount: int
    IsFavorite: bool
    Played: bool


class EmbyItem(BaseModel):
    Name: str
    ServerId: str
    Id: str
    CanDelete: bool
    SupportsSync: bool
    Container: str
    RunTimeTicks: int
    ProductionYear: int
    IsFolder: bool
    Type: str
    UserData: EmbyUserData
    PrimaryImageAspectRatio: float
    ImageTags: Dict[str, str]
    BackdropImageTags: List[str]
    MediaType: str


class EmbySearchResult(BaseModel):
    Items: List[EmbyItem]
    TotalRecordCount: int
