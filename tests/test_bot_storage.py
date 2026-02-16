import pytest

from bot.bot_storage import get_last_sent_id, save_last_sent_news_id, get_news_after_id, get_all_users


@pytest.mark.asyncio
async def test_get_last_sent_id(async_session):
    """Проверка id последней отправленой новости"""
    chat_id = 100

    last_id = await get_last_sent_id(chat_id, async_session)
    assert last_id == 0, "id последней отпрвленной новости должен быть равен 0, если нет отправленных новостей"

    await save_last_sent_news_id(chat_id=chat_id, last_id=10, session=async_session)
    last_id = await get_last_sent_id(chat_id, async_session)
    assert last_id == 10, "id последней отпрвленной новости должен быть равен 10"


@pytest.mark.asyncio
async def test_get_news_after_id(async_session, news_list):
    """Получение новостей"""
    news = await get_news_after_id(last_id=0, session=async_session)
    assert len(news) == 2, "Должно быть получено 2 новости"
    assert news[0].title == "Test Title 1", "Заголовок первой новости должен быть 'Test Title 1'"
    assert news[1].title == "Test Title 2", "Заголовок второй новости должен быть 'Test Title 2'"


@pytest.mark.asyncio
async def test_get_all_users(async_session):
    """Получение пользователей"""
    await save_last_sent_news_id(chat_id=111, last_id=11, session=async_session)
    await save_last_sent_news_id(chat_id=222, last_id=22, session=async_session)

    users = await get_all_users(async_session)
    assert len(users) == 2, "Должно быть 2 пользователя в базе"
    assert users[0] == 111, "id первого юзера должен быть 111"
    assert users[1] == 222,  "id второго юзеера должен быть 222"
