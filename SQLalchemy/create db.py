import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from config import settings


def create_db(db_name):
    """Создание базы данных"""
    # Устанавливаем соединение с postgres
    connection = psycopg2.connect(user=settings.POSTGRESQL_USERNAME, password=settings.POSTGRESQL_PASSWORD)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Создаем курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    sql_create_database = cursor.execute(db_name)  # Создаем базу данных
    # Закрываем соединение
    cursor.close()
    connection.close()


create_db("test tasks")

