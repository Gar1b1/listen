from sqlalchemy import Integer, String, Column, ForeignKey, UniqueConstraint
from database import Base


class Song(Base):
    __tablename__ = 'song'
    uuid = Column(Integer, primary_key=True)
    artist = Column(String, ForeignKey('artist.name'), nullable=False)
    name = Column(String, nullable=False)
    mp3_path = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint('artist', 'name', name='uix_artist_name'),
    )

    def __init__(self, artist, name, mp3_path):
        self.artist = artist
        self.name = name
        self.mp3_path = mp3_path
