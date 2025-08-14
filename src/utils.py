import re

import pandas as pd


from datetime import datetime #, timedelta


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


'''def get_month_to_date(date_str: str):
    """Возвращает (первое_числа_месяца, указанная_дата)"""
    input_date = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")  # .date()
    first_day = input_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return first_day.strftime("%d-%m-%Y %H:%M:%S"), input_date'''

# Возвращает строки с картами по указанный период начиная с 1-го числа месяца.
def get_card_from_period(var: list, date: str):
    if not isinstance(var, list) or not all(isinstance(item, dict) for item in var):
        raise ValueError("var должен быть списком словарей")

    df = pd.DataFrame(var)

    # Конвертация дат
    try:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        end_date = pd.to_datetime(date, format="%d-%m-%Y %H:%M:%S")
        first_day = end_date.replace(day=1)  # Первый день месяца
    except Exception as e:
        raise ValueError(f"Ошибка в формате даты: {e}")

    data_frame = df[(df["Дата операции"] > first_day) & (df["Дата операции"] < end_date)]

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

    return result

# Возвращает ТОП 10 транзакций
def get_top_transactions(var: list, date: str):
    if not isinstance(var, list) or not all(isinstance(item, dict) for item in var):
        raise ValueError("var должен быть списком словарей")
    # first_day, dates = get_month_to_date(date)

    df = pd.DataFrame(var)

    # Конвертация дат
    try:
        df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
        end_date = pd.to_datetime(date, format="%d-%m-%Y %H:%M:%S")
        first_day = end_date.replace(day=1)  # Первый день месяца
    except Exception as e:
        raise ValueError(f"Ошибка в формате даты: {e}")

    data_frame = df[(df["Дата операции"] > first_day) & (df["Дата операции"] <= end_date)].copy()
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

    return res


# Функция для извлечения номеров
def extract_phones(text):
    pattern = r'(?:\+7|8|7)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    return re.findall(pattern, str(text))



# Функция для извлечения Имён
def extract_name_parts(text):
    pattern = r'''
        \b                          # Граница слова
        [А-ЯЁA-Z][а-яёa-z]+         # Имя (с заглавной, затем строчные)
        \s                          # Пробел
        [А-ЯЁA-Z]                   # Инициал фамилии (1 заглавная буква)
        (?:\.|\b)                   # Точка или граница слова
        (?![а-яёa-z])               # Не должно быть строчных после инициала
    '''
    return re.findall(pattern, str(text), flags=re.X | re.IGNORECASE)

    #matches = re.finditer(pattern, str(text))
    #return [f"{match.group(1)} {match.group(2)}." for match in matches]

