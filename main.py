from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException
from database.crud import *
from database.models import *


from typing import List

import base64

app = FastAPI(
    title="MusicStack",
    description="Advance music rating platform",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files to '/public' or another non-root path
app.mount("/static", StaticFiles(directory="static"), name="static")


def is_token_valid(token: str):
    if token is None:
        return False

    token = token.split('|')
    if len(token) != 2:
        return False

    userName, userPass = token[0], token[1]

    info = get_userinfo(userName)

    if info is None:
        return False

    return info.Password == userPass


@app.get("/")
async def read_index():
    return FileResponse('static/index.html')


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse("static/index.html")


@app.get('/api/index/{top_n}')
async def index(top_n: int) -> IndexData:
    # Make sure this function actually returns an IndexData object
    return get_index_data(top_n)

@app.get('/api/recommend/{user_id}')
async def get_recommendations(user_id: int) -> AlbumRecommendationList:
    try:
        data = get_recommend_album_by_user_id(user_id)
        print(data)
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/api/get_token')
async def get_token(user_name: str, user_pass: str) -> Message:
    user_info = get_userinfo(user_name)
    if user_info is None:
        return Message(
            flag=False,
            msg="user name not exist",
        )
    else:
        if user_info.Password != user_pass:
            return Message(
                flag=False,
                msg="incorrect password",
            )
        else:
            token = user_name + '|' + user_pass
            return Message(
                flag=True,
                msg="ok",
                content=token
            )


@app.get('/api/search/{album_name}')
async def search(album_name: str) -> List[AlbumCover]:
    return search_album(album_name)


@app.get('/api/user/{user_id}/followers')
async def get_followers(user_id: int) -> List[str]:
    return get_follower_by_userid(user_id)


@app.get('/api/user/{user_id}/following')
async def get_following(user_id: int) -> List[str]:
    return get_following_by_userid(user_id)


@app.post('/api/user/{follower_id}/unfollow/{followee_id}')
async def unfollow_user(follower_id: int, followee_id: int) -> Message:
    try:
        unfollow_userid(follower_id, followee_id)
        return Message(flag=True, msg="Successfully unfollowed.")
    except Exception as e:
        return Message(flag=False, msg=str(e))


@app.get('/api/user/{user_id}/playlists')
async def get_playlists(user_id: int) -> List[str]:
    return get_user_playlist(user_id)


@app.post('/api/token/{token}')
async def valid_token(token: str) -> bool:
    return is_token_valid(token)


@app.get('/api/get_userid/{user_name}')
async def get_userid(user_name: str) -> int:
    user_info = get_userinfo(user_name)
    if user_info is not None:
        return user_info.UserID
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post('/api/user/{follower_id}/follow/{followee_id}')
async def api_follow_userid(follower_id: int, followee_id: int):
    try:
        follow_userid(follower_id, followee_id)
        return {"message": "Followed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/api/user/{user_id}/playlist/add/{playlist_name}')
async def api_add_playlist(user_id: int, playlist_name: str):
    try:
        add_playlist(user_id, playlist_name)
        return {"message": "Playlist created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/api/user/{user_id}/playlist/remove/{playlist_name}')
async def api_remove_playlist(user_id: int, playlist_name: str):
    try:
        remove_playlist(user_id, playlist_name)
        return {"message": "Playlist removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/api/album/{album_id}')
async def get_album_detail(album_id: int) -> AlbumDetail:
    return get_album_details_by_id(album_id)


@app.get('/api/artist/{artist_id}')
async def get_artist_info(artist_id: int) -> ArtistDetail:
    return get_artist_detail(artist_id)
class RatingRequest(BaseModel):
    user_id: int
    rating: int
@app.post('/api/rate/album/{album_id}')
async def rate_an_album(album_id: int, rating_request: RatingRequest):
    try:
        rate_album(rating_request.user_id, album_id, rating_request.rating)
        return {"message": "Album rated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/rate/album/{album_id}")
async def read_album_rate():
    return FileResponse('static/pages/album_rate.html')
class TrackRatingRequest(BaseModel):
    user_id: int
    rating: int

@app.post('/api/rate/track/{track_id}')
async def rate_track_api(track_id: int, rating_request: TrackRatingRequest):
    try:
        rate_track(rating_request.user_id, track_id, rating_request.rating)
        return {"message": "Track rated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.get("/rate/track")
async def read_track_rate():
    return FileResponse('static/pages/track_rate.html')

