from SQLalchemy.models import create_tables
from parser.parser import start_parsing
from services import interval_parsing
from telegram.telegram_bot import start_bot

if __name__ == "__main__":
    create_tables()  # Создаем таблицы в бд
    interval_parsing(60)  # Запускаем парсинг с периодичностью в час
    start_bot()
