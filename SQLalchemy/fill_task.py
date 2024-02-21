import asyncio
import json

from SQLalchemy.CRUD import add_task, search_double
from SQLalchemy.models import Tasks, Tags


def task_collector(d):

    """Собирает задачу и тег"""
    task = Tasks(
        contestId=d["contestId"],
        index_task=d["index"],
        name=d["name"],
        type=d["type"],
        solved_count=d["solved_count"]
    )

    tags = [Tags(task=task, tag=tag) for tag in d["tags"]]

    search = [str(d["contestId"]), d["index"]]
    if search_double(Tasks, search):  # Проверка дубликатов
        add_task(task, tags)


def save_task_in_db():
    """Добавление задач в бд"""
    with open("tasks.json", "r", encoding="utf-8") as rf:
        data = json.load(rf)
        for d in data:
            task_collector(d)
        print("данные о задаче внесены в БД")
