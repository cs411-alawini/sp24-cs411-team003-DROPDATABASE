import sys

from fastapi import FastAPI

from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.crud import *
from database.models import *

app = FastAPI(
    title="MusicStack",
    description="advance music rating platform",
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

# app.include_router(blog.router, prefix="/blog", tags=["blog"])



@app.get('/api/index/{top_n}')
async def get_index_data(top_n: int) -> IndexData:
    return get_index_data(top_n)


@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse("static/index.html")


app.mount("/", StaticFiles(directory="static", html=True), name="static")
