import json
import time
import asyncio
from asyncio import sleep

import schedule
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from SQLalchemy.CRUD import add_task, add_one
from SQLalchemy.models import Tasks, Tags
from config import settings
from parser.parser import start_parsing

engine = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRESQL_USERNAME}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOSTNAME}/{settings.POSTGRESQL_DATABASE}",
    echo=True, pool_size=100, max_overflow=100)
session = Session(bind=engine)


def search_double(bd, search_data):
    """Проверка на повторы"""
    data_in_db = []
    for data in session.query(bd).all():
        *add_in_db, _ = (str(data)).split(", ")
        data_in_db.append(add_in_db)
    if search_data in data_in_db:
        return True
    else:
        return False


async def task_collector(d):
    """Собирает задачу и тег, затем добавляет в БД"""
    task = Tasks(
        contestId=d["contestId"],
        index_task=d["index"],
        name=d["name"],
        type=d["type"],
        solved_count=d["solved_count"]
    )

    tags = [Tags(task=task, tag=tag) for tag in d["tags"]]

#    search = [str(d["contestId"]), d["index"]]
#    if search_double(ProblemStatistics, search):  # Проверка дубликатов
    add_task(task, tags)
    await sleep(.1)


async def save_task_in_db():
    """Если задачи нет в БД то добавляем ее"""
    with open("tasks.json", "r", encoding="utf-8") as rf:
        data = json.load(rf)
        steck = 200
        tasks = []

        for d in data:
            tasks.append(asyncio.create_task(task_collector(d)))
            if len(tasks) == steck:
                await asyncio.gather(*tasks)
                tasks = []
        print("данные о задаче внесены в БД")


loop = asyncio.get_event_loop()
loop.run_until_complete(save_task_in_db())


def interval_parsing(interval):
    """Запуск периодического парсинга и созжанение в бд"""
    schedule.every(interval).minutes.do(start_parsing())
    while True:
        schedule.run_pending()
        time.sleep(1)
