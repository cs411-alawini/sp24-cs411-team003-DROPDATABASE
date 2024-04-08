from pydantic import BaseModel
from typing import List


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


