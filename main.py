from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.crud import get_index_data, get_userinfo, search_album
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
