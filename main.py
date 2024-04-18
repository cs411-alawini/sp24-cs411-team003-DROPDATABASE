from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.crud import get_index_data
from database.models import IndexData

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
