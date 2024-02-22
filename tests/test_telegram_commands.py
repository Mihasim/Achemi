import pytest

from telegram.commands import TelegramInterface


@pytest.fixture
def commands():
    return TelegramInterface()


def test_format_message(commands):
    task_data = ["Название", 1, "А1", "ТИП", ["tag"], 12]
    assert commands.format_message(task_data) == (f"Название задачи Название, Id соревнования {1}, "
                                                  f"индекс задачи в соревновании 'А1', тип ТИП, "
                                                  f"теги ['tag'], колличество решений {12}")


def test_search_for_tag(commands):
    data = commands.search_for_tag("graphs", 1000, 5000)
    assert isinstance(data, list)
    assert data != []
    nothing_data = commands.search_for_tag("brad", 1000, 5000)
    assert nothing_data == ['По запросу ничего не найдено']


def test_search_for_name(commands):
    data = commands.search_for_name('Final Countdown')
    assert isinstance(data, str)
