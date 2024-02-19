import random

from SQLalchemy.CRUD import Searching


class TelegramInterface:

    def format_message(self, task_data: list):
        message = (f"Название задачи {task_data[0]}, Id соревнования {task_data[1]}, "
                   f"индекс задачи в соревновании '{task_data[2]}', тип {task_data[3]}, "
                   f"теги {task_data[4]}, сложность {task_data[5]}")
        return message

    def search_for_tag(self, tag: str, min_difficult: int, max_difficult: int) -> list:
        searching = Searching()
        task_list = []
        for task in searching.search_tags(tag):
            if max_difficult >= task[5] >= min_difficult:
                task_list.append(task)
        if len(task_list) >= 10:
            messages = random.sample(task_list, 10)
        else:
            messages = random.sample(task_list, len(task_list))
        list_format_message = []
        for message_ in messages:
            list_format_message.append(self.format_message(message_))
        return list_format_message

    def search_for_name(self, name: str) -> str:
        searching = Searching()
        message = self.format_message(searching.search_name(name)[0])
        return message




#test = TelegramInterface()
#print(test.search_for_tag('graphs', 0, 1000))
#test.search_for_name('One-Dimensional Puzzle')
