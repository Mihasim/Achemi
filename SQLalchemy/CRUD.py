import random

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import settings

from SQLalchemy.models import Tasks, Tags

engine = create_engine(
    f"postgresql+psycopg2://{settings.POSTGRESQL_USERNAME}:{settings.POSTGRESQL_PASSWORD}@{settings.POSTGRESQL_HOSTNAME}/{settings.POSTGRESQL_DATABASE}",
    echo=True, pool_size=6, max_overflow=10)
# дополнительные аргументы-ключевые слова, которые можно передать в функцию create_engine()
# echo - Если задать True, то движок будет сохранять логи SQL в стандартный вывод. По умолчанию значение равно False
# pool_size - Определяет количество соединений для пула. По умолчанию — 5
# max_overflow - Определяет количество соединений вне значения pool_size. По умолчанию — 10
# encoding - Определяет кодировку SQLAlchemy. По умолчанию — UTF-8. Однако этот параметр не влияет на
# кодировку всей базы данных
# isolation_level - Уровень изоляции. Эта настройка контролирует степень изоляции одной транзакции.
# Разные базы данных поддерживают разные уровни.

session = Session(bind=engine)


def add_one(one) -> None:
    """Функция для добавления одного объекта в бд"""
    session.add(one)  # Добавление экземпляра объекта в сессию
    session.commit()  # Сохранение экземпляра в бд


def add_all(all_obj: list) -> None:
    """Функция для добавления списка объектов в бд"""
    session.add_all(all_obj)  # Добавление списка экземпляров объектов в сессию
    session.commit()  # Сохранение экземпляра в бд


def add_task(task, tag_list: list) -> None:
    """Добавление одной задачи"""
    add_one(task)
    add_all(tag_list)


class Searching:
    def __init__(self):
        self.tasks = session.query(Tasks)

    def search_name(self, task_name: str) -> list:
        """Поиск задач по названию"""
        prompt = self.tasks.filter(Tasks.name == task_name)
        print("По запросу найдено:")
        answers = []
        for answer in prompt:
            answers.append([answer.name,
                            answer.contestId,
                            answer.index_task,
                            answer.type,
                            answer.tags,
                            answer.solved_count]
                           )
        return answers

    def search_tags(self, tag: str) -> list:
        """Поиск задач по тегам"""
        prompt = self.tasks.join(Tags).filter(Tags.tag == tag)
        print("По запросу найдено:")
        answers = []
        for answer in prompt:
            tags = [str(tags_) for tags_ in list(answer.tags)]
            print(tag, tags)
            if tag in tags:
                answers.append([answer.name,
                                answer.contestId,
                                answer.index_task,
                                answer.type,
                                answer.tags,
                                answer.solved_count]
                               )
        return answers

searching = Searching()
# searching.search_difficulty(1000)
print(searching.search_name("One-Dimensional Puzzle"))
# print(searching.search_tags('graphs'))
