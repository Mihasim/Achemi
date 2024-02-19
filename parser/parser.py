import json
from typing import Any

import requests


class Parser:
    def __init__(self, url: str):
        self.url = url

    def tasks_collector(self) -> tuple[Any, Any]:
        """Получение данных о задачах в архиве codeforces
        и возврат их в виде списка словарей"""
        response = requests.get(self.url)
        if response.status_code == 200:
            data_statistic = response.json()["result"]["problemStatistics"]
            data_tasks = response.json()["result"]["problems"]
            return data_tasks, data_statistic
        else:
            print("Ошибка получения данных о задачах в архиве codeforces", response.status_code)

    def data_processing(self) -> tuple[Any, Any]:
        """Обработка данных полученных с сайта
        Получаем необходимую информацию о задаче
        """
        tasks, statistics = self.tasks_collector()

        statistic_list_dict = []
        for data in statistics:
            # Информация о статистике
            statistic_info = {
                "contestId": data["contestId"],
                "index_task": data["index"],
                "solved_count": data["solvedCount"],
            }
            statistic_list_dict.append(statistic_info)

        tasks_list_dict = []
        for data in tasks:
            # Информация о задаче
            tasks_info = {
                "contestId": data["contestId"],
                "index": data["index"],
                "name": data["name"],
                "tags": data["tags"],
                "type": data["type"]
            }
            tasks_list_dict.append(tasks_info)

        return tasks_list_dict, statistic_list_dict

    @staticmethod
    def save_data_json(tasks: list, file_name: str) -> None:
        """Сохранение данных в файл json"""
        with open(f"../{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f)
        print("Данные сохранены")


def start_parsing():
    """Запуск парсера и сохранение данных"""
    print("Начат парсинг")
    url_codeforces = f"https://codeforces.com/api/problemset.problems"
    parser = Parser(url_codeforces)
    data_tasks, data_statistic = parser.data_processing()
    parser.save_data_json(data_tasks, "tasks")
    parser.save_data_json(data_statistic, "statistic")
    print("Парсинг окончен")


start_parsing()
