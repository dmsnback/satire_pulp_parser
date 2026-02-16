from satire_pulp_parser.spider_storage import is_news_exists, save_news


def test_save_and_check_news(session, news):
    """Проверяет что новостей нет в базе,
    сохранение новости
    и новость появилась в базе после сохранения."""
    assert not is_news_exists(news['url'], session), "Перед сохраением новой новости её не должно быть в базе"
    save_news(news["url"], news["title"], news['image'], news["text"], session=session)
    assert is_news_exists(news["url"], session), "Новость должна появиться в базе после сохранения"
