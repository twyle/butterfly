from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.orm import sessionmaker
from ...config.config import BaseConfig
from contextlib import contextmanager
from flask import current_app


class Base(MappedAsDataclass, DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URI = BaseConfig().db_conn_string
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def create_all():
    Base.metadata.create_all(bind=engine)
    
def drop_all():
    Base.metadata.drop_all(bind=engine)

@contextmanager
def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()
    
