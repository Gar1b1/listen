from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from .songs.router import router as songs_router
from .artists.router import router as artists_router
from .playlists.router import router as playlists_router
from .users.router import router as users_router
from config import config


class Router(BaseModel):
    router: APIRouter
    prefix: str
    tags: list[str]
    model_config = ConfigDict(arbitrary_types_allowed=True)


routers: list[Router] = [
    Router(router=users_router, prefix="/users", tags=config.USERS_TAGS),
    Router(router=songs_router, prefix="/songs", tags=config.SONGS_TAGS),
    Router(router=artists_router, prefix="/artists", tags=config.ARTISTS_TAGS),
    Router(router=playlists_router, prefix="/playlists", tags=config.PLAYLISTS_TAGS)
]
