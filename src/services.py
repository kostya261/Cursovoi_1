import pandas as pd

from src.loader import excel_loader
from src.utils import extract_phones, extract_name_parts


def search_phone(data, date):

    df = pd.DataFrame(data)

    # Конвертация дат
    try:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        end_date = pd.to_datetime(date, format="%d-%m-%Y %H:%M:%S")
        first_day = end_date.replace(day=1)  # Первый день месяца
    except Exception as e:
        raise ValueError(f"Ошибка в формате даты: {e}")

    data_frame = df[(df["Дата операции"] > first_day) & (df["Дата операции"] < end_date)]

    #phones_mask = data_frame["Описание"].str.contains(phone_pattern, regex=True, na=False)
    has_phone = data_frame["Описание"].apply(
        lambda x: len(extract_phones(x)) > 0
    )
    result = data_frame[has_phone]

    #print(data_frame)
    return result.to_json(orient='records', force_ascii=False, indent=2)




def search_name(data, date):
    name_pattern = r'\b[А-ЯЁ][а-яё]+ [А-ЯЁ]\.\b'

    df = pd.DataFrame(data)

    # Конвертация дат
    try:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        end_date = pd.to_datetime(date, format="%d-%m-%Y %H:%M:%S")
        first_day = end_date.replace(day=1)  # Первый день месяца
    except Exception as e:
        raise ValueError(f"Ошибка в формате даты: {e}")

    data_frame = df[(df["Дата операции"] > first_day) & (df["Дата операции"] < end_date)]

    has_name = data_frame["Описание"].apply(
        lambda x: len(extract_name_parts(x)) > 0
    )
    result = data_frame[has_name]

    #print(data_frame)
    return result.to_json(orient='records', force_ascii=False, indent=2)



def search_line(data, date: str, search_str):
    df = pd.DataFrame(data)

    # Конвертация дат
    try:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        end_date = pd.to_datetime(date, format="%d-%m-%Y %H:%M:%S")
        first_day = end_date.replace(day=1)  # Первый день месяца
    except Exception as e:
        raise ValueError(f"Ошибка в формате даты: {e}")

    data_frame = df[(df["Дата операции"] > first_day) & (df["Дата операции"] < end_date)]

    # Поиск в указанных столбцах
    result = data_frame[
        data_frame['Категория'].str.contains(search_str, case=False, na=False) |
        data_frame['Описание'].str.contains(search_str, case=False, na=False)
        ]
    return result.to_json(orient='records', force_ascii=False, indent=2)


def convert_data(data, date):
    df = pd.DataFrame(data)
    # Конвертация дат
    try:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        end_date = pd.to_datetime(date, format="%d-%m-%Y %H:%M:%S")
        first_day = end_date.replace(day=1)  # Первый день месяца
        #return first_day, end_date
        return df[(df["Дата операции"] > first_day) & (df["Дата операции"] < end_date)]
    except Exception as e:
        raise ValueError(f"Ошибка в формате даты: {e}")


if __name__ == "__main__":
    excel_file = excel_loader("..\\data\\operations.xlsx")
    #print(search_line(excel_file, "25-11-2020 12:50:00", "Магнит"))
    print()
    #print(search_phone(excel_file, "25-11-2021 12:50:0"))
    print()
    #print(search_name(excel_file, "15-11-2021 12:50:0"))
    print(convert_data(excel_file, "25-11-2020 12:50:00"))
