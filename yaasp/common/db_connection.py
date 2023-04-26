from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from yaasp.config import ENABLE_SQLALCHEMY_LOGGING, DB_FILE

Base = declarative_base()
db_engine = create_engine(f'sqlite:///{DB_FILE}', echo=ENABLE_SQLALCHEMY_LOGGING)
Session = sessionmaker(bind=db_engine)
session_object = Session()
