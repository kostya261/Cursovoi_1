# Курсовой проект на SkyEng
## Описание:
Приложение для анализа транзакций, которые находятся в Excel-файле.

## Установка:

1. Клонируйте репозиторий:
   [ссылка](https://github.com/kostya261/PythonProject/pull/3)
   
3. Зависимости указанные в файле: *pyproject.toml*
```
[tool.poetry]
name = "cursovoi_1"
version = "0.1.0"
description = ""
authors = ["Konstantin Kosarew <kos26193@gmail.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.13"
poetry-core = "^2.1.3"
shell = "^1.0.1"
python-dotenv = "^1.1.1"
pandas = "^2.3.1"
openpyxl = "==3.2.0b1"
pandas-stubs = "^2.3.0.250703"
requests = "^2.32.4"
typing-extensions = "^4.14.1"
pytest = "^8.4.1"
flake8 = "==7.3.0"
mypy = "==1.17.1"
numpy = "==2.3.2"
coverage = "==7.10.4"
certifi = "==2025.8.3"
click = "==8.2.2"
urllib3 = "==2.5.0"
pytest-cov = "==6.2.1"
finnhub-python = "==2.4.24"
charset-normalizer = "==3.4.3"
types-pytz = "==2025.2.0.20250809"


[tool.poetry.group.dev.dependencies]
requests = "^2.32.3"
pytest = "^8.3.5"
pytest-cov = "^6.1.1"
pytest-mock = "^3.14.1"


[tool.poetry.group.lint.dependencies]
flake8 = "^7.2.0"
mypy = "^1.15.0"
black = "^25.1.0"
isort = "^6.0.1"


[tool.black]
# Максимальная длина строки
line-length = 119
# Файлы, которые не нужно форматировать
exclude = """ \\.git """


[tool.isort]
# максимальная длина строки
line_length = 119


[tool.mypy]
disallow_untyped_defs = true
warn_return_any = true
exclude = 'venv'


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


```

## Использование:

Откройте проект например в PyCharm, откройте файл main.py и запустите его.
По желанию можно его всячески модифицировать в рамках тестирования написанных функций.

В Cursovoi_1\src описаны семь модулей:
**loader.py, saver.py, external_api.py, utils.py, reports.py, services.py, views.py**, которые и реализуют весь скромный функционал курсового проекта.

### loader.py
В модуле loader.py описаны функции *excel_loader* и *load_json*
обе функции выполняют загрузку файлов:

*excel_loader* - загружает excel файлы
Принимает на входе строку с именем файла.
На выходе DataFrame

*load_json* - Загружает json файлы
Принимает на входе строку с именем файла.
На выходе json данные

Примеры использования:
```
temp_result = excel_load("operations.xcls")
print(temp_result)
```

```
temp_result = load_json("operations.json")
print(temp_result)
```

### saver.py
В данном модуле описана функция: 

*save_json* - которая принимает на вход строку с именем файла и json данными
после чего сохраняет данные на диск



Пример использования:
```
save_json("name_file.json", json_data)
```


### reports.py
*spending_by_category* - выполняет поиск категории и возвращает DataFrame 


Пример использования:
```
excel_file = excel_loader("..\\data\\operations.xlsx")
print(spending_by_category(excel_file, "Перевод", "03-11-2019 00:50:00", filename="C:\\temp\\test.xlsx"))
```


## services.py
Содержит три функции, которые выполняют поиск данных в DataFrame
search_phone
search_name
search_line

Пример использования:
```
excel_file = excel_loader("..\\data\\operations.xlsx")
data = convert_data(excel_file, "25-11-2021 12:50:00")
print(search_line(data, "Магнит"))
print(search_line(pd.DataFrame(excel_file), "Супермаркеты"))
print(search_phone(data))
print(search_name(data))
```


## utils.py
Данный модуль содержит больше всего функций
*get_time_based_greeting* - в зависимости от времени суток выдает соответствующее приветствие 
*convert_data* - конвертирует дату и делает выборку в DataFrame от 1-го по указанное число
*filter_by_date* - Работает примерно как предыдущая функция, но работает с начальной и конечной датой
так же фильтруя DataFrame в указанных пределах. Если конечная дата не передана, то к начальной дате просто 
прибавляются 3 месяца
*get_card_from_period* - Возвращает строки с номерами карт
*get_top_transactions* - Возвращает ТОП 10 транзакций
*extract_phones* - Функция для извлечения номеров
*extract_name_parts* - Функция для извлечения Имён


## external_api.py
*currency_rate* - выясняет курс валют
*get_stock_price* - выясняет курсы акций
*currency_rates* - передаёт -> currency_rate - список валют, по которым необходимо выяснить курс 


## views.py
*main_page* - Принимает параметром дату и время после чего формирует json данные согласно шаблону 
в задании к курсовой.


## Тесты
Добавлены тестовые файлы test_widget.py, test_masks.py, test_processing.py, test_generators.py
которые проверяют ранее написанные функции.
В них реализованы функции:


Тест запускается из командной строки, командой **pytest**

## Лицензия:

В данном конкретном случае вероятно её ещё нет 8-/
