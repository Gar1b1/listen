from locale import normalize

from fastapi import APIRouter, status, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.exc import NoResultFound, IntegrityError
import os

from database.models.artist import Artist
from database.models.song import Song
from database import db
from config import config

router = APIRouter()


def __make_sure_artist_exists(session, artist_name: str):
    session.query(Artist).filter_by(name=artist_name).one()


def serve_song_file(path_to_song: str):
    path = os.path.join(config.SONGS_BASE_PATH, path_to_song)
    if not os.path.isfile(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MP3 file not found")
    return FileResponse(path, media_type='audio/mpeg', filename=path_to_song)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_song(song_name, artist_name: str, song_file: UploadFile):
    try:
        if song_file.content_type != "audio/mpeg":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only MP3 files are allowed (content type check failed)"
            )

        song_file.file.seek(0)
        header = song_file.file.read(3)
        song_file.file.seek(0)  # Reset file pointer for future reading

        if header not in [b"ID3", b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is not a valid MP3 (magic byte check failed)"
            )

        with db.session() as session:
            __make_sure_artist_exists(session, artist_name)
            song = Song(name=song_name, artist=artist_name, mp3_path="")
            session.add(song)
            session.flush()
            file_name = f"{song.uuid}.mp3"
            song.mp3_path = file_name
            full_path = os.path.join(config.SONGS_BASE_PATH, file_name)
            with open(full_path, "wb") as f:
                f.write(song_file.file.read())
            session.commit()
            return "Song Created Successfully"
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Song with the name: {song_name} already exists to this artist"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{artist_name}/{song_name}", status_code=status.HTTP_200_OK)
def get_song_by_artist(artist_name: str, song_name: str):
    try:
        with db.session() as session:
            artists = session.query(Artist).filter_by(name=artist_name).one_or_none()
            if artists is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found")
            song = session.query(Song).filter_by(name=song_name, artist=artist_name).one()
            return serve_song_file(song.mp3_path)

    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Song with name: {song_name} not found to artist {artist_name}")
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{song_uuid}", status_code=status.HTTP_200_OK)
def get_song_by_uuid(song_uuid: str):
    try:
        with db.session() as session:
            song = session.query(Song).filter_by(uuid=song_uuid).one()
            return serve_song_file(song.mp3_path)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Song with uuid: {song_uuid} not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("", status_code=status.HTTP_200_OK)
def get_all_songs():
    try:
        with db.session() as session:
            songs = session.query(Song).all()
            return songs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
