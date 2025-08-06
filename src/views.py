from datetime import datetime


def main_page(date_time: str) -> None:
    hello: str = get_time_based_greeting()
    json_result: dict = {"greeting": hello, "cards": []}
    print(json_result)


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


if __name__ == "__main__":
    print(get_time_based_greeting())
