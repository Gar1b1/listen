from fastapi import APIRouter
from database import db
from database.models import Playlist, User
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import NoResultFound, IntegrityError

from database.models.artist import Artist
from database.models.playlist import PlaylistToSongs
from database.models.song import Song
from config import config

router = APIRouter()


def __make_sure_user_exists(session, user_id):
    session.query(User).filter_by(user_id=user_id).one()


def __make_sure_artist_exists(session, artist_name):
    session.query(Artist).filter_by(name=artist_name).one()


def __make_sure_song_exists(session, song_id):
    song = session.query(Song).filter_by(uuid=song_id).one_or_none()
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")


def __make_sure_playlist_exists(session, playlist_id):
    playlist = session.query(Playlist).filter_by(uuid=playlist_id).one_or_none()
    if not playlist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")


@router.post("", status_code=status.HTTP_201_CREATED)
def create_playlist(creator_id: str, playlist_name: str):
    try:
        with db.session() as session:
            __make_sure_user_exists(session, creator_id)
            session.add(Playlist(creator=creator_id, name=playlist_name))
            session.commit()
        return "Playlist Created Successfully"
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Creator not found")
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Playlist with the name: {playlist_name} already exists to this user"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/user_playlists/{user_id}", status_code=status.HTTP_200_OK)
def get_user_playlists(user_id: str):
    try:
        with db.session() as session:
            __make_sure_user_exists(session, user_id)
            playlists = session.query(Playlist).filter_by(creator=user_id).all()
        return {"user": user_id, "playlist": playlists}
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/add_song/{playlist_id}/{song_id}", status_code=status.HTTP_200_OK, tags=[config.SONGS_TAGS])
def add_song_to_playlist(playlist_id: str, song_id: str):
    try:
        with db.session() as session:
            __make_sure_playlist_exists(session, playlist_id)
            __make_sure_song_exists(session, song_id)
            session.add(PlaylistToSongs(playlist_id=playlist_id, song_id=song_id))
            session.commit()
            return "Song Added Successfully"
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Song already in playlist")
    except Exception as e:
        if type(e) is HTTPException:
            raise e
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/remove_song/{playlist_id}/{song_id}", status_code=status.HTTP_200_OK, tags=[config.SONGS_TAGS])
def remove_song_from_playlist(playlist_id: str, song_id: str):
    try:
        with db.session() as session:
            __make_sure_playlist_exists(session, playlist_id)
            __make_sure_song_exists(session, song_id)
            playlist_to_song = session.query(PlaylistToSongs).filter_by(playlist_id=playlist_id, song_id=song_id).one()
            session.delete(playlist_to_song)
            session.commit()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not in playlist")


@router.get("/{playlist_id}/songs")
def get_playlist_songs(playlist_id: str):
    try:
        with db.session() as session:
            session.query(Playlist).filter_by(uuid=playlist_id).one()
            songs = session.query(PlaylistToSongs).filter_by(playlist_id=playlist_id).all()
            return {"songs": songs}
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Playlist not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
