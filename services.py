import time
import schedule

from SQLalchemy.models import create_tables
from parser.parser import Parser
from SQLalchemy.fill_task import save_task_in_db
from telegram.telegram_bot import start_bot


def start_parsing() -> None:
    """Запуск парсера и сохранение данных"""
    print("Начат парсинг")
    url_codeforces = "https://codeforces.com/api/problemset.problems"
    parser = Parser(url_codeforces)
    data_tasks = parser.data_processing()
    parser.save_data_json(data_tasks, "tasks")
    print("Парсинг окончен")

    save_task_in_db()  # Сохраняем данные в бд


create_tables()  # Пересоздаем таблицы в бд
start_parsing()  # Парсим данные
start_bot()  # Запускаем бота


"""Запуск периодического парсинга и созжанение в бд"""
schedule.every(60).minutes.do(start_parsing)
while True:
    schedule.run_pending()
    time.sleep(1)
