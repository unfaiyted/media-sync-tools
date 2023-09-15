from pydantic import BaseModel
from typing import Dict, List, Optional

from enum import Enum

class JellyfinItemType(Enum):
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


class JellyfinImageType(Enum):
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


class JellyfinUserData(BaseModel):
    PlaybackPositionTicks: int
    PlayCount: int
    IsFavorite: bool
    Played: bool
    Key: str


class JellyfinItem(BaseModel):
    Name: str
    ServerId: str
    Id: str
    CanDelete: bool
    HasSubtitles: bool
    Container: str
    PremiereDate: Optional[str]
    CriticRating: Optional[float]
    OfficialRating: Optional[str]
    ChannelId: Optional[str]
    CommunityRating: Optional[float]
    RunTimeTicks: int
    ProductionYear: int
    IsFolder: bool
    Type: str
    UserData: JellyfinUserData
    PrimaryImageAspectRatio: float
    VideoType: str
    ImageTags: Dict[str, str]
    BackdropImageTags: List[str]
    ImageBlurHashes: Dict[str, Dict[str, str]]
    LocationType: str
    MediaType: str


class JellyfinSearchResult(BaseModel):
    Items: List[JellyfinItem]
    TotalRecordCount: int
    StartIndex: int


# Usage:
# data = {...} # your json result from Jellyfin
# result = JellyfinSearchResult(**data)
