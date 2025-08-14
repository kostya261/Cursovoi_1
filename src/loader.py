import json
from pathlib import Path
from typing import Dict

import pandas as pd


def excel_loader(file_path: str = "") -> list[Dict]:
    """
    Функция читает файл формата xlsx и возвращает список со словарями

    :param file_path: - путь к файлу
    :return: - Список словарей с данными.
    """
    try:
        result = pd.read_excel(file_path).to_dict(orient="records")
        return result
    except FileNotFoundError:
        raise ValueError("Ошибка!")
    except pd.errors.ParserError:
        raise ValueError("Неверный XLSX формат")


def load_json(file_path: str = "", debug: bool = False) -> dict:

    path = Path(file_path)
    # Проверка существования файла
    if not path.is_file():
        # logger.error(f"\nИмя: {__name__} transaction_loader - нет имени файла!")
        if debug:
            print(f"\nИмя: {__name__} load_json - нет имени файла!")
        return {}

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        # print(data)
        if isinstance(data, dict):
            # logger.info(f"\nИмя: {__name__} transaction_loader - Ok!")
            if debug:
                print(f"\nИмя: {__name__} load_json - Ok!")
            return data
        return {}

    except (json.JSONDecodeError, UnicodeDecodeError):
        # Обработка ошибок: пустой файл, битый JSON или проблемы с кодировкой
        # logger.debug(f"\nИмя: {__name__} transaction_loader - пустой файл, битый JSON или проблемы с кодировкой!")
        if debug:
            print(f"\nИмя: {__name__} load_json - пустой файл, битый JSON или проблемы с кодировкой!")
        return {}
