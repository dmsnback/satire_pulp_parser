import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


DATABASE_URL_SYNC = os.getenv("DATABASE_URL_SYNC")


engine = create_engine(DATABASE_URL_SYNC)

SessionLocal = sessionmaker(engine)
