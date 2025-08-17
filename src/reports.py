import logging
from functools import wraps
from pathlib import Path
from typing import Optional
import pandas as pd

from config import logs_reports_file
from src.loader import excel_loader
from src.utils import filter_by_date



#описание логера
logger = logging.getLogger(__name__)

log_dir = Path(__file__).parent.parent
log_dir.mkdir(exist_ok=True)

file_handler = logging.FileHandler(logs_reports_file, "w+", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)



"""
Сохранение в файл по умолчанию:
result = spending_by_category(df, "Магнит", filename=True)
# Сохранит в spending_report.json


Сохранение в указанный файл:
result = spending_by_category(df, "Магнит", filename="магазины.csv")
# Сохранит в магазины.csv


Без сохранения:
result = spending_by_category(df, "Магнит")
# Не сохраняет в файл
"""
def save_to_file(default_filename: str = "spending_report.json"):
    """
    Декоратор для сохранения результатов в файл.

    Args:
        default_filename: Имя файла по умолчанию
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Отделяем filename от других kwargs
            filename = kwargs.pop('filename', None)

            # Вызываем оригинальную функцию
            result = func(*args, **kwargs)

            # Если указано сохранить в файл
            if filename:
                final_filename = filename if isinstance(filename, str) else default_filename

                # Определяем формат по расширению
                if final_filename.endswith('.json'):
                    result.to_json(final_filename, orient='records', force_ascii=False)
                elif final_filename.endswith('.csv'):
                    result.to_csv(final_filename, index=False, encoding='utf-8')
                elif final_filename.endswith('.xlsx'):
                    result.to_excel(final_filename, index=False)
                else:
                    final_filename = f"{final_filename}.json"
                    result.to_json(final_filename, orient='records', force_ascii=False)

                print(f"Данные сохранены в: {final_filename}")

            return result
        return wrapper
    return decorator


@save_to_file(default_filename="spending_report.json")
def spending_by_category(
        data_frame: pd.DataFrame,
        category: str,
        start_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает расходы по указанной категории, начиная с заданной даты.

    Параметры:
    - data_frame: DataFrame с транзакциями
    - category: Название категории для поиска
    - start_date: Дата начала периода

    Возвращает:
    - DataFrame с отфильтрованными записями
    """
    try:
        # Фильтрация по дате
        filtered_df = filter_by_date(data_frame, start_date)

        # Фильтрация по категории (регистронезависимый поиск)
        result = filtered_df[
            filtered_df["Категория"].str.contains(category, case=False, na=False)
        ]

        # Если ничего не найдено, возвращаем пустой DataFrame с теми же колонками
        if result.empty:
            logger.info(f"\nИмя файла: {__name__}, имя функции spending_by_category - Ок")
            return pd.DataFrame(columns=data_frame.columns)
        logger.info(f"\nИмя файла: {__name__}, имя функции spending_by_category - Ок")
        return result

    except Exception as e:
        # В случае ошибки возвращаем пустой DataFrame с оригинальными колонками
        print(f"Ошибка при фильтрации: {str(e)}")
        logger.error(f"\nИмя файла: {__name__}, имя функции spending_by_category - Ошибка при фильтрации: {str(e)}")
        return pd.DataFrame(columns=data_frame.columns)


if __name__ == "__main__":
    excel_file = excel_loader("..\\data\\operations.xlsx")
    print(spending_by_category(excel_file, "Перевод", "03-11-2019 00:50:00", filename="C:\\temp\\test.xlsx"))
