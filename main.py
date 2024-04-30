from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.crud import get_index_data, get_userinfo, search_album, get_follower_by_userid, get_following_by_userid, \
    get_user_playlist, unfollow_userid, get_user_playlist
from database.models import IndexData, Message, AlbumCover

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

