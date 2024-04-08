import sys

from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import os


STATIC_MOUNT_DIR = "./static"

app = FastAPI(
    title="MusicStack",
    description="advance music rating platform",
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

if not os.path.isdir(STATIC_MOUNT_DIR):
    print(
        "\033[91m"
        "static mounting point detached, please re-download the source code"
        "and drag the /static folder into the project directory"
        "\033[0m"
    )
    sys.exit(1)

app.mount("/", StaticFiles(directory=STATIC_MOUNT_DIR, html=True), name='static')

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(blog.router, prefix="/blog", tags=["blog"])

@app.get("/", include_in_schema=False)
async def index():
    """
    server index page

    """
    return FileResponse("index.html")