from datetime import datetime

from pydantic import BaseModel
from typing import Optional, Union


# https://trakt.docs.apiary.io/#reference/search/text-query/get-text-query-results
# Models are based on this result documentation
class TraktIDs(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.tvrage = None

    trakt: int
    slug: str
    imdb: Optional[str]
    tmdb: Optional[int]
    tvdb: Optional[int]


class Movie(BaseModel):
    title: str
    year: int
    ids: TraktIDs


class Show(BaseModel):
    title: str
    year: int
    ids: TraktIDs


class Episode(BaseModel):
    season: int
    number: int
    title: str
    ids: TraktIDs


class Person(BaseModel):
    name: str
    ids: TraktIDs


class User(BaseModel):
    username: str
    private: bool
    name: str
    vip: bool
    vip_ep: bool
    ids: TraktIDs


class TraktList(BaseModel):
    name: str
    description: str
    privacy: str
    share_link: str
    type: str
    display_numbers: bool
    allow_comments: bool
    sort_by: str
    sort_how: str
    created_at: str
    updated_at: str
    item_count: int
    comment_count: int
    likes: int
    ids: TraktIDs
    user: User


class TraktItem(BaseModel):
    type: str
    score: Optional[float]
    listed_at: Optional[datetime]
    notes: Optional[str]
    movie: Optional[Movie]
    show: Optional[Show]
    episode: Optional[Episode]
    person: Optional[Person]
    list: Optional[TraktList]

    def get_item(self) -> Union[Movie, Show, Episode, Person, TraktList]:
        if self.movie:
            return self.movie
        elif self.show:
            return self.show
        elif self.episode:
            return self.episode
        elif self.person:
            return self.person
        elif self.list:
            return self.list
        else:
            raise ValueError("No valid item type found!")
