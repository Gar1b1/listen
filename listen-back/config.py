from enum import Enum
import os


class BaseConfig:
    HOST: str
    PORT: int
    DOCS_ROUTE: str
    SONGS_BASE_PATH: str
    SONGS_TAGS = ["songs"]
    USERS_TAGS = ["users"]
    PLAYLISTS_TAGS = ["playlists"]
    ARTISTS_TAGS = ["artists"]


class DEV_CONFIG(BaseConfig):
    HOST: str = "localhost"
    PORT: int = 8080
    DOCS_ROUTE: str = "/docs"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database/example.db"
    SONGS_BASE_PATH: str = "D:\documents\pytn\listen\songs"




class EnvConfig:
    DEV: str = "Development"
    PROD: str = "Production"


def get_config(env: str) -> BaseConfig:
    if env == EnvConfig.DEV:
        return DEV_CONFIG
    elif env == EnvConfig.PROD:
        return "Production"
    else:
        raise Exception(f"Unknown env: {env}")


config: BaseConfig = get_config(os.getenv("ENV", EnvConfig.DEV))
