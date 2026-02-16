<a name="Начало"></a>

## Satire Pulp Parser

![Satire Pulp parser](https://github.com/dmsnback/satire_pulp_parser/actions/workflows/main.yml/badge.svg) ![Python](https://img.shields.io/badge/python-3.11-blue) ![Tests](https://img.shields.io/badge/tests-pytest-brightgreen) ![Black](https://img.shields.io/badge/code%20style-black-000000) ![License](https://img.shields.io/badge/license-MIT-green)


- [Описание](#Описание)
- [Технологии](#Технологии)
- [Тестирование](#Тестирование)
- [Шаблон заполнения .env-файла](#Шаблон)
- [Запуск проекта](#Запуск)
- [Автор](#Автор)

<a name="Описание"></a>

### Описание

Проект представляет собой парсер сатирических новостей с сайта [Панорама](https://panorama.pub/ "Перейти") и Telegram-бот для автоматической рассылки новых публикаций пользователям.

**Возможности:**
```md
    - Парсинг новостей с сайта panorama.pub  
    - Сохранение новостей в PostgreSQL  
    - Автоматическая рассылка новых новостей через Telegram-бот
    - Планировщик запуска парсера каждые 20 минут
    - Асинхронная работа бота с данными
```

Парсер написан с использованием **Scrapy**, **SQLAlchemy**, **PostgreSQL** и **Python Telegram Bot**

В проекте настроен **CI pipeline** с использованием **GitHub Actions**:

```md
- Автоматическая проверка кода (black, isort, flake8)
- Запуск unit-тестов (`pytest`)
- Сборка Docker-образа
- Публикация образа в **Docker Hub** при пуше в соответствующие ветки
```

```md
Проект адаптирован для использования **PostgreSQL** и развёртывания в контейнерах **Docker**.
```

> [Вернуться в начало](#Начало)

<a name="Технологии"></a>

### Технологии

[![Python](https://img.shields.io/badge/Python-1000?style=for-the-badge&logo=python&logoColor=ffffff&labelColor=000000&color=000000)](https://www.python.org)
[![Scrapy](https://img.shields.io/badge/Scrapy-1000?style=for-the-badge&logo=scrapy&logoColor=ffffff&labelColor=000000&color=000000)](https://docs.scrapy.org/en/latest/index.html)
[![python_telegram_bot](https://img.shields.io/badge/python_telegram_bot-1000?style=for-the-badge&logo=telegram&logoColor=ffffff&labelColor=000000&color=000000)](https://docs.python-telegram-bot.org/en/stable/index.html)
[![Postgres](https://img.shields.io/badge/Postgres-1000?style=for-the-badge&logo=postgresql&logoColor=ffffff&labelColor=000000&color=000000)](https://www.postgresql.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1000?style=for-the-badge&logo=sqlalchemy&logoColor=ffffff&labelColor=000000&color=000000)](https://www.sqlalchemy.org)
[![Docker](https://img.shields.io/badge/Docker-1000?style=for-the-badge&logo=docker&logoColor=ffffff&labelColor=000000&color=000000)](https://www.docker.com)
[![Pytest](https://img.shields.io/badge/Pytest-1000?style=for-the-badge&logo=pytest&logoColor=ffffff&labelColor=000000&color=000000)](https://docs.pytest.org/en/stable/index.htmlc)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=ffffff&labelColor=000000&color=000000)](https://github.com/features/actions)

> [Вернуться в начало](#Начало)

<a name="Тестирование"></a>

### Тестирование

В проекте реализованы **unit-тесты** с использованием `pytest`.

Запуск тестов локально:

```python
pytest -v
```

> [Вернуться в начало](#Начало)

<a name="Шаблон"></a>

### Шаблон заполнения .env-файла

> `env.example` с дефолтными значениями расположен в корневой папке

```python
TELEGRAM_TOKEN=1234567890:Telegram-Token  # Токен Telegram бота
DATABASE_URL_SYNC = postgresql+psycopg2://postgres:postgres@db:5432/satire_pulp_db  # Указываем адрес БД (Синхронная версия)
DATABASE_URL_ASYNC=postgresql+asyncpg://postgres:postgres@db:5432/satire_pulp_db # Указываем адрес БД (Асинхронная версия)
POSTGRES_DB = satire_pulp_db # Имя базы дданных
POSTGRES_USER = postgres # Имя юзера PostgreSQL
POSTGRES_PASSWORD = yourpassword # Пароль юзера PostgreSQL
POSTGRES_HOST=db # Имя сервиса PostgreSQL в docker-compose
POSTGRES_PORT=5432 # Порт PostgreSQL внутри контейнера
```

> [Вернуться в начало](#Начало)

<a name="Запуск"></a>

### Запуск проекта на локальной машине

- Склонируйте репозиторий

```python
git clone git@github.com:dmsnback/satire_pulp_parser.git
```

- Установите и активируйте виртуальное окружение

```python
python3 -m venv venv
```

Для `Windows`

```python
source venv/Scripts/activate
```

Для `Mac/Linux`

```python
source venv/bin/activate
```

- Установите зависимости из файла
`requirements.txt`

```python
python3 -m pip install --upgrade pip
```

```python
pip install -r requirements.txt
```

- Запускаем Docker контейнеры (db, bot)

```python
docker-compose up -d db bot         
```

- Создаём таблицы в БД

```python
docker-compose exec bot python -m db.init_db       
```

- Перезапускаем Docker контейнеры

```python
docker-compose up -d        
```

- После запуска запустите бота командой ```/start```

> Команда ```/show_news``` пришлёт последние 10 новостей из базы, если они ещё не были отправлены, далее бот будет присылать только новые новости, которые появятся на сайте.

> [Вернуться в начало](#Начало)

<a name="Автор"></a>

### Автор

- [Титенков Дмитрий](https://github.com/dmsnback)

> [Вернуться в начало](#Начало)
