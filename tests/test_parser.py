import json

import pytest

from parser.parser import Parser


@pytest.fixture
def parser_data():
    return Parser("https://codeforces.com/api/problemset.problems")


def test_tasks_collector(parser_data):
    assert isinstance(parser_data.tasks_collector(), tuple)


def test_data_processing(parser_data):
    assert isinstance(parser_data.data_processing(), tuple)


def test_save_tasks_data_json(parser_data):
    """
    Проверка соответствует ли содержание файла тому что необходимо было сохранить
    """
    with open("../tasks.json", "r", encoding="utf-8") as rf:
        data = json.load(rf)
        data_tasks, data_statistic = parser_data.data_processing()
        parser_data.save_data_json(data_tasks, "tasks")
        assert json.dumps(data_tasks) == json.dumps(data)


def test_save_statistic_data_json(parser_data):
    """
    Проверка соответствует ли содержание файла тому что необходимо было сохранить
    """
    with open("../statistic.json", "r", encoding="utf-8") as rf:
        data = json.load(rf)
        data_tasks, data_statistic = parser_data.data_processing()
        parser_data.save_data_json(data_statistic, "statistic")
        assert json.dumps(data_statistic) == json.dumps(data)
