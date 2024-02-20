import json

import pytest

from parser.parser import Parser


@pytest.fixture
def parser_data():
    return Parser("https://codeforces.com/api/problemset.problems")


def test_tasks_collector(parser_data):
    parser_data_ = parser_data.tasks_collector()
    assert isinstance(parser_data_, list)
    assert parser_data_ != []


def test_data_processing(parser_data):
    parser_data_ = parser_data.data_processing()
    assert isinstance(parser_data_, list)
    assert parser_data_ != []


def test_save_tasks_data_json(parser_data):
    """
    Проверка соответствует ли содержание файла тому что необходимо было сохранить
    """
    with open("tasks.json", "r", encoding="utf-8") as rf:
        data = json.load(rf)
        data_tasks = parser_data.data_processing()
        parser_data.save_data_json(data_tasks, "tasks")
        assert json.dumps(data_tasks) == json.dumps(data)
