import logging
import re
from datetime import datetime  # , timedelta
from pathlib import Path

import pandas as pd
from dateutil.relativedelta import relativedelta

from config import logs_utils_file

# описание логера
logger = logging.getLogger(__name__)

log_dir = Path(__file__).parent.parent
log_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler(logs_utils_file, "w+", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


# Приветствие в зависимости от времени суток
def get_time_based_greeting() -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= current_hour < 17:
        greeting = "Добрый день"
    elif 17 <= current_hour < 23:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"

    return greeting


def convert_data(data_frame: pd.DataFrame, date: str):
    """
    Фильтрует DataFrame c первого числа месяца по указанную дату.

    Параметры:
        - data_frame: Исходный DataFrame
        - date: Конечная дата
    Возвращает:
        - Отфильтрованный DataFrame
    """
    if data_frame.empty:
        logger.error(f"\nИмя файла: {__name__}, имя функции convert_data - Передан пустой DataFrame")
        raise ValueError("Передан пустой DataFrame")
    try:
        df = pd.DataFrame(data_frame)
        # Конвертация дат
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        end_date = pd.to_datetime(date, format="%d-%m-%Y %H:%M:%S")
        first_day = end_date.replace(day=1, hour=0, minute=0, second=0)
        logger.info(f"\nИмя файла: {__name__}, имя функции convert_data - Ок")
        return df[(df["Дата операции"] >= first_day) & (df["Дата операции"] < end_date)]
    except Exception as e:
        logger.error(f"\nИмя файла: {__name__}, имя функции convert_data - Ошибка в формате даты: {e}")
        raise ValueError(f"Ошибка в формате даты: {e}")


def filter_by_date(data_frame: pd.DataFrame, start_date: str = None, end_date: str = None):
    """
    Фильтрует DataFrame по диапазону дат.

    Параметры:
    - data_frame: Исходный DataFrame
    - start_date: Начальная дата (строка или None)
        Может быть в форматах:
        "dd.mm.YYYY HH:MM:SS"
        "dd-mm-YYYY HH:MM:SS"
        "YYYY-mm-dd HH:MM:SS"
    - end_date: Конечная дата (аналогичные форматы или None)

    Возвращает:
    - Отфильтрованный DataFrame
    """
    if data_frame.empty:
        logger.error(f"\nИмя файла: {__name__}, имя функции filter_by_date - Передан пустой DataFrame")
        raise ValueError("Передан пустой DataFrame")

    try:
        # Создаем копию DataFrame
        df = data_frame.copy()

        # Конвертируем колонку с датами (с автоматическим определением формата)
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True, format="mixed")

        # Функция для конвертации входных дат
        def parse_date(date_str):
            if date_str is None:
                return None
            try:
                logger.info(f"\nИмя файла: {__name__}, имя функции filter_by_date - Ок")
                return pd.to_datetime(date_str, dayfirst=True)
            except Exception as e:
                logger.info(f"\nИмя файла: {__name__}, имя функции filter_by_date - {e}")
                return pd.to_datetime(date_str)

        # Обрабатываем start_date
        start_date = parse_date(start_date) if start_date else df["Дата операции"].min()

        # Обрабатываем end_date
        if end_date is None:
            end_date = start_date + relativedelta(months=3)
        else:
            end_date = parse_date(end_date)

        # Фильтруем данные
        mask = (df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)
        logger.info(f"\nИмя файла: {__name__}, имя функции filter_by_date - Ок")
        return df[mask]

    except Exception as e:
        logger.error(f"\nИмя файла: {__name__}, имя функции filter_by_date - Ошибка фильтрации по дате: {str(e)}")
        raise ValueError(f"Ошибка фильтрации по дате: {str(e)}")


# Возвращает строки с картами по указанный период начиная с 1-го числа месяца.
def get_card_from_period(data_frame: pd.DataFrame):
    """
    На самом деле период указывается в любой другой функции которая фильтрует DataFrame по дате
    здесь же только вывод карт.
    """
    if data_frame.empty:
        logger.error(f"\nИмя файла: {__name__}, имя функции get_card_from_period - Передан пустой DataFrame")
        raise ValueError("Передан пустой DataFrame")

    total_spent = data_frame.groupby("Номер карты")["Сумма операции с округлением"].sum().reset_index()
    num_card = list(total_spent["Номер карты"])
    sum_card = list(total_spent["Сумма операции с округлением"])
    cache = list(round(total_spent["Сумма операции с округлением"] / 100, 2))

    result: list = []

    for i in range(0, len(num_card)):

        result.append(
            {
                "last_digits": num_card[i][1:],
                "total_spent": sum_card[i],
                "cashback": cache[i],
            }
        )
    logger.info(f"\nИмя файла: {__name__}, имя функции get_card_from_period - Ок")
    return result


# Возвращает ТОП 10 транзакций
def get_top_transactions(data_frame: pd.DataFrame):

    top_categories = data_frame["Категория"].value_counts().head(10).to_dict()

    result: list = []

    for category, value in top_categories.items():
        result.append(category)

    res: list = []

    for value in result:
        row = data_frame.loc[data_frame["Категория"] == value].iloc[0]
        date_str = row["Дата операции"].strftime("%d.%m.%Y")
        res.append(
            {
                "date": date_str,
                "amount": float(row["Сумма операции"]),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    logger.info(f"\nИмя файла: {__name__}, имя функции get_top_transactions - Ок")
    return res


# Функция для извлечения номеров
def extract_phones(text: str):
    pattern = r"(?:\+7|8|7)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
    logger.info(f"\nИмя файла: {__name__}, имя функции extract_phones - Ок")
    return re.findall(pattern, str(text))


# Функция для извлечения Имён
def extract_name_parts(text: str):
    pattern = r"""
        \b                          # Граница слова
        [А-ЯЁA-Z][а-яёa-z]+         # Имя (с заглавной, затем строчные)
        \s                          # Пробел
        [А-ЯЁA-Z]                   # Инициал фамилии (1 заглавная буква)
        (?:\.|\b)                   # Точка или граница слова
        (?![а-яёa-z])               # Не должно быть строчных после инициала
    """
    logger.info(f"\nИмя файла: {__name__}, имя функции extract_name_parts - Ок")
    return re.findall(pattern, str(text), flags=re.X)
