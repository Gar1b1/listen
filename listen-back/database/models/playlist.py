from sqlalchemy import Integer, String, Column, ForeignKey, UniqueConstraint
from database import Base


class Playlist(Base):
    __tablename__ = 'playlist'
    uuid = Column(Integer, primary_key=True)
    creator = Column(String, ForeignKey('user.user_id'), nullable=False)
    name = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('creator', 'name', name='uix_creator_name'),
    )

    def __init__(self, creator, name):
        self.creator = creator
        self.name = name


class PlaylistToSongs(Base):
    __tablename__ = 'playlist_to_songs'
    uuid = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlist.uuid'), nullable=False)
    song_id = Column(Integer, ForeignKey('song.uuid'), nullable=False)
    __table_args__ = (
        UniqueConstraint('playlist_id', 'song_id', name='uix_playlist_song'),
    )

    def __init__(self, playlist_id, song_id):
        self.playlist_id = playlist_id
        self.song_id = song_id
