import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from db.models import Base, News


DATABASE_SYNC_URL = "sqlite:///:memory:"
DATABASE_ASYNC_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
def session():
    engine = create_engine(DATABASE_SYNC_URL, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()
    yield session
    session.close()


@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine(DATABASE_ASYNC_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    AsyncSession = async_sessionmaker(engine, expire_on_commit=False)
    async with AsyncSession() as async_session:
        yield async_session
    await engine.dispose()


@pytest.fixture
def news():
    test_news = {
        'url': 'https://panorama.pub/test-news',
        'title': 'Test Title',
        'text': 'Test Text',
        'image': None
    }
    return test_news


@pytest_asyncio.fixture
async def news_list(async_session):
    first_news = News(url="https://panorama.pub/test-news_1", title="Test Title 1", image=None, text="Ttest Text_1")
    second_news = News(url="https://panorama.pub/test-news_2", title="Test Title 2", image=None, text="Ttest Text_2")

    async_session.add_all([first_news, second_news])
    await async_session.commit()

    return [first_news, second_news]
