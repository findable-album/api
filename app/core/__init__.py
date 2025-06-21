from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import close_db, connect_db
from app.core.search_model import get_search_model
from app.routes.image import router as image_router


async def start():
    await connect_db()


async def shutdown():
    await close_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_search_model()
    await start()

    yield

    await shutdown()


app = FastAPI(debug=True, lifespan=lifespan)

app.mount('/static', StaticFiles(directory='static'), name='static')


app.include_router(image_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
