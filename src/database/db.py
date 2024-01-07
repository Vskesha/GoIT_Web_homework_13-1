from fastapi import status, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.conf.config import settings

DB_URI = settings.sqlalchemy_database_url
engine = create_engine(DB_URI)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
