from symtable import Class

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from config import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class DB:
    @staticmethod
    def session():
        class SessionManager:
            def __enter__(self):
                self.db = session_local()
                return self.db

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.db.close()

        return SessionManager()


db = DB()
