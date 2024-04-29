from pydantic import BaseModel, HttpUrl
from typing import List, Optional


class AlbumRating(BaseModel):
    AlbumTitle: str
    AvgRating: float


class AlbumRecommendation(BaseModel):
    AlbumTitle: str
    ArtistName: str


class AlbumRecommendationList(BaseModel):
    recommendations: List[AlbumRecommendation]


class TrackRating(BaseModel):
    TrackName: str
    AvgRating: float


class PopularTracksResponse(BaseModel):
    tracks: List[TrackRating]


class AlbumCover(BaseModel):
    AlbumID: int
    AlbumTitle: str
    ArtistName: str
    AlbumCover: Optional[HttpUrl] = "https://api.cirno.me/anipic/"


class ArtistCover(BaseModel):
    ArtistID: int
    ArtistName: str
    ArtistCover: Optional[HttpUrl] = "https://api.cirno.me/anipic/"


class IndexData(BaseModel):
    TopAlbum: List[AlbumCover]
    TopArtists: List[ArtistCover]


class Message(BaseModel):
    flag: bool
    content: Optional[str]
    msg: Optional[str]


class UserInfo(BaseModel):
    UserID: int
    UserName: str
    Password: str


class UserAlbumRate(BaseModel):
    AlbumID: int
    AlbumTitle: str
    Rating: int
