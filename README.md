Для запуска проекта необходибо: 

-заполнить данные в файле config.py

-создать базу данных "codeforces tasks" 

-запустить файл main.py

При запуске приложения: 

-в базе данных создаются таблицы, 

-происходит парсинг данных и сохранение данных в файлы .json,

-данные из файлов переносятся в соответствующие таблицы

-запускается переодический парсинг (раз в час)

-запускается телеграмм бот

При отправки сообщения боту он дает список команд.

(название задачи и теги при запросе писать только на английском языке.)