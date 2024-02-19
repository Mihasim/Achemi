import json
import time

import schedule
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from SQLalchemy.CRUD import add_task, add_one
from SQLalchemy.models import Tasks, Tags, ProblemStatistics
from config import settings
from parser.parser import start_parsing

engine = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRESQL_USERNAME}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOSTNAME}/{settings.POSTGRESQL_DATABASE}",
    echo=True, pool_size=6, max_overflow=10)
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


def save_to_bd():
    """Если задачи нет в БД то добавляем ее"""
    with open("../tasks.json", "r", encoding="utf-8") as rf:
        data = json.load(rf)
        for d in data:
            task = Tasks(
                contestId=d["contestId"],
                index_task=d["index"],
                name=d["name"],
                type=d["type"]
            )

            tags = [Tags(task=task, tag=tag) for tag in d["tags"]]

            search = [str(d["contestId"]), d["index"]]
            if search_double(ProblemStatistics, search):  # Проверка дубликатов
                add_task(task, tags)
        print("данные о задаче внесены в БД")

    with open("../statistic.json", "r", encoding="utf-8") as rf:
        data = json.load(rf)

        for d in data:
            statistic = ProblemStatistics(
                contestId=d["contestId"],
                index_task=d["index_task"],
                solved_count=d["solved_count"],
            )
            search = [str(d["contestId"]), d["index_task"]]
            if search_double(ProblemStatistics, search):  # Проверка дубликатов
                add_one(statistic)
        print("данные о статистике внесены в БД")


def interval_parsing(interval):
    """Запуск периодического парсинга и созжанение в бд"""
    schedule.every(interval).minutes.do(start_parsing(), save_to_bd())
    while True:
        schedule.run_pending()
        time.sleep(1)

save_to_bd()