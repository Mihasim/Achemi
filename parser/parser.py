import json

import requests


class Parser:
    def __init__(self, url: str):
        self.url = url

    def tasks_collector(self) -> list:
        """Получение данных о задачах в архиве codeforces
        и возврат их в виде списка словарей"""
        response = requests.get(self.url)
        if response.status_code == 200:
            data_statistic = response.json()["result"]["problemStatistics"]
            data_tasks = response.json()["result"]["problems"]
            i = 0
            for data_task in data_tasks:
                data_task["solved_count"] = data_statistic[i]["solvedCount"]
                i += 1
            return data_tasks
        else:
            print("Ошибка получения данных о задачах "
                  "в архиве codeforces", response.status_code)

    def data_processing(self) -> list:
        """Обработка данных полученных с сайта
        Получаем необходимую информацию о задаче
        """
        tasks = self.tasks_collector()

        tasks_list_dict = []
        for data in tasks:
            # Информация о задаче
            tasks_info = {
                "contestId": data["contestId"],
                "index": data["index"],
                "name": data["name"],
                "tags": data["tags"],
                "type": data["type"],
                "solved_count": data["solved_count"]
            }
            tasks_list_dict.append(tasks_info)

        return tasks_list_dict

    @staticmethod
    def save_data_json(tasks: list, file_name: str) -> None:
        """Сохранение данных в файл json"""
        with open(f"{file_name}.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f)
        print("Данные сохранены")
