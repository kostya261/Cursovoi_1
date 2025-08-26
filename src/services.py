import logging
import pandas as pd
from pathlib import Path

from config import logs_services_file
from src.loader import excel_loader
from src.utils import convert_data, extract_name_parts, extract_phones

# описание логера
logger = logging.getLogger(__name__)

log_dir = Path(__file__).parent.parent
log_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler(logs_services_file, "w+", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def search_phone(data_frame: pd.DataFrame) -> str:
    """
    Поиск всех номеров телефонов

    :param data_frame:
    :return: - json data
    """
    # Проверка данных
    if data_frame.empty:
        logger.error(f"\nИмя файла: {__name__}, имя функции search_phone - Передан пустой DataFrame")
        raise ValueError("Передан пустой DataFrame")
    has_phone = data_frame["Описание"].apply(lambda x: len(extract_phones(x)) > 0)
    result = data_frame[has_phone]
    logger.info(f"\nИмя файла: {__name__}, имя функции search_phone - Ок")
    return result.to_json(orient="records", force_ascii=False, indent=2)


def search_name(data_frame: pd.DataFrame) -> str:
    """
    Поиск всех имён

    :param data_frame:
    :return: - json data
    """
    # Проверка данных
    if data_frame.empty:
        logger.error(f"\nИмя файла: {__name__}, имя функции search_name - Передан пустой DataFrame")
        raise ValueError("Передан пустой DataFrame")
    has_name = data_frame["Описание"].apply(lambda x: len(extract_name_parts(x)) > 0)
    result = data_frame[has_name]
    logger.info(f"\nИмя файла: {__name__}, имя функции search_name - Ок")
    return result.to_json(orient="records", force_ascii=False, indent=2)


def search_line(data_frame: pd.DataFrame, search_str: str) -> str:
    """
    Поиск по указанному слову в Категории и Описании

    :param data_frame:
    :param search_str: - Строка для поиска
    :return: - json data
    """
    # Проверка данных
    if data_frame.empty:
        logger.error(f"\nИмя файла: {__name__}, имя функции search_line - Передан пустой DataFrame")
        raise ValueError("Передан пустой DataFrame")
    # Поиск в cтолбцах Категория и Описание
    result = data_frame[
        data_frame["Категория"].str.contains(search_str, case=False, na=False)
        | data_frame["Описание"].str.contains(search_str, case=False, na=False)
    ]
    logger.info(f"\nИмя файла: {__name__}, имя функции search_line - Ок")
    return result.to_json(orient="records", force_ascii=False, indent=2)


if __name__ == "__main__":
    excel_file = excel_loader("..\\data\\operations.xlsx")
    data = convert_data(excel_file, "25-11-2021 12:50:00")
    print(search_line(data, "Магнит"))
    print(search_line(pd.DataFrame(excel_file), "Супермаркеты"))
    print()
    print(search_phone(data))
    print()
    print(search_name(data))
