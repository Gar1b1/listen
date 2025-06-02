from sqlalchemy import Integer, String, Column, ForeignKey, UniqueConstraint
from database import Base


class Artist(Base):
    __tablename__ = 'artist'
    uuid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
