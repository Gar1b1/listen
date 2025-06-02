from fastapi import APIRouter, status, HTTPException
from sqlalchemy.exc import IntegrityError, NoResultFound

from database.models.artist import Artist
from database import db
from config import config
from database.models.song import Song

router = APIRouter()


@router.post("/{artist_name}", status_code=status.HTTP_201_CREATED)
def create_artist(artist_name: str):
    try:
        with db.session() as session:
            session.add(Artist(name=artist_name))
            session.commit()
            return "Artist Created Successfully"
    except IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Artist with the name: {artist_name} already exists")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{artist_name}", status_code=status.HTTP_200_OK)
def get_artist(artist_name: str):
    try:
        with db.session() as session:
            artist = session.query(Artist).filter_by(name=artist_name).one()
            return {"Artist": artist}
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Artist with name: {artist_name} not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{artist_name}/songs", status_code=status.HTTP_200_OK, tags=config.SONGS_TAGS)
def get_artist_songs(artist_name: str):
    try:
        with db.session() as session:
            session.query(Artist).filter_by(name=artist_name).one()
            songs = session.query(Song).filter_by(name=artist_name).all()
            return {"Songs": songs}
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Artist with name: {artist_name} not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
