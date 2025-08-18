import json
import logging
from pathlib import Path

import pandas as pd

from config import logs_loader_file

# описание логера
logger = logging.getLogger(__name__)

log_dir = Path(__file__).parent.parent
log_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler(logs_loader_file, "w+", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def excel_loader(file_path: str = "") -> pd.DataFrame:
    """
    Функция читает файл формата xlsx и возвращает список со словарями

    :param file_path: - путь к файлу
    :return: - Список словарей с данными.
    """
    try:
        result = pd.read_excel(file_path)  # .to_dict(orient="records")
        logger.info(f"\nИмя: {__name__} excel_loader - Ok!")
        return result
    except FileNotFoundError:
        logger.error(f"\nИмя: {__name__} excel_loader - файл не существует!")
        raise ValueError("Ошибка!")
    except pd.errors.ParserError:
        logger.error(f"\nИмя: {__name__} excel_loader - Неверный XLSX формат!")
        raise ValueError("Неверный XLSX формат")


def load_json(file_path: str = "", debug: bool = False) -> dict:

    path = Path(file_path)
    # Проверка существования файла
    if not path.is_file():
        logger.error(f"\nИмя: {__name__} load_json - нет имени файла!")
        if debug:
            print(f"\nИмя: {__name__} load_json - нет имени файла!")
        return {}

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        # print(data)
        if isinstance(data, dict):
            logger.info(f"\nИмя: {__name__} load_json - Ok!")
            if debug:
                print(f"\nИмя: {__name__} load_json - Ok!")
            return data
        return {}

    except (json.JSONDecodeError, UnicodeDecodeError):
        # Обработка ошибок: пустой файл, битый JSON или проблемы с кодировкой
        logger.debug(f"\nИмя: {__name__} load_json - пустой файл, битый JSON или проблемы с кодировкой!")
        if debug:
            print(f"\nИмя: {__name__} load_json - пустой файл, битый JSON или проблемы с кодировкой!")
        return {}
