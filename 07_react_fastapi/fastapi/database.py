from dotenv.parser import decode_escapes
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

URL_DATABASE = os.getenv("URL_DATABASE")

engine = create_engine(URL_DATABASE,connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()