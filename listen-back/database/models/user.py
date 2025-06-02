from sqlalchemy import Integer, String, Column
from database import Base


class User(Base):
    __tablename__ = 'user'
    uuid = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, unique=True)

    def __init__(self, user_id):
        self.user_id = user_id
