import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv()


DATABASE_URL_ASYNC = os.getenv("DATABASE_URL_ASYNC")


engine = create_async_engine(DATABASE_URL_ASYNC, echo=False)


AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
