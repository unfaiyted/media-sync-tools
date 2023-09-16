from typing import List, Dict, Any
from pydantic import BaseModel

class TmdbCreatedBy(BaseModel):
    gravatar_hash: str
    id: str
    name: str
    username: str

class TmdbMovieDetails(BaseModel):
    adult: bool
    backdrop_path: str
    genre_ids: List[int]
    id: int
    media_type: str
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str
    release_date: str
    title: str
    video: bool
    vote_average: float
    vote_count: int

class TmdbList(BaseModel):
    average_rating: float
    backdrop_path: str
    comments: Dict[str, Any]  # Since all values are null, using Any for now
    created_by: TmdbCreatedBy
    description: str
    id: int
    iso_3166_1: str
    iso_639_1: str
    name: str
    object_ids: Dict[str, str]
    page: int
    poster_path: str
    public: bool
    results: List[TmdbMovieDetails]

class TmdbSearchResult(BaseModel):
    page: int
    results: List[TmdbMovieDetails]
    total_pages: int
    total_results: int
