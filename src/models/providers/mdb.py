from pydantic import BaseModel
from typing import Optional


class MdbItem(BaseModel):
    id: int
    rank: int
    adult: int
    title: str
    imdb_id: str
    tvdb_id: Optional[str]
    language: str
    mediatype: str
    release_year: int
    spoken_language: str


class MdbList(BaseModel):
    id: int
    name: str
    slug: str
    items: int
    likes: int
    user_id: int
    mediatype: str
    user_name: str
    description: Optional[str]
