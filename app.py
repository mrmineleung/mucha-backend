from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import openapi_tags
from controller.auth_controller import auth_controller_router
from controller.chart_controller import chart_controller_router
from controller.playlist_controller import playlist_controller_router
from controller.user_controller import user_controller_router
import os
from dotenv import load_dotenv

from db import init_db
from extensions import scheduler
from jobs import tasks
from logging import getLogger

logger = getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    scheduler.start()
    tasks.init()
    logger.info("Created Schedule Object")
    yield


app = FastAPI(lifespan=lifespan, openapi_tags=openapi_tags.tags_metadata)
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


# Include the routers from controller modules
app.include_router(user_controller_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth_controller_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chart_controller_router, prefix="/api/v1/charts", tags=["Charts"])
app.include_router(playlist_controller_router, prefix="/api/v1/playlists", tags=["Playlists"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run("app:app", host=os.environ.get("HOST"), port=int(os.environ.get("PORT")), reload=True)
