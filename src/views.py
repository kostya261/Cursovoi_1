import json

from config import file_path, user_settings_file
from src.external_api import currency_rates, get_stock_price
from src.loader import excel_loader, load_json
from src.utils import convert_data, get_card_from_period, get_time_based_greeting, get_top_transactions


def main_page(date_time: str) -> str:
    """
    Данная функция читает файлы user_settings.json и operations.xlsx
    выводит отсортированные результаты по различным транзакциям отсортированным
    по именам, телефонным номерам и категориям за указанный в date_time промежуток времени.
    так же выясняются курсы валют указанные в user_settings.json и информация по акциям,
    которые так же перечисленны в данном файле.
    :param date_time: - вдата, до которой выводится информация начиная с первого числа
                        указанного месяца
    :return:
    """
    result: dict = {}

    excel_file = excel_loader(file_path)
    data = convert_data(excel_file, date_time)
    json_file = load_json(user_settings_file)

    user_currencies = json_file.get("user_currencies", [])
    if not isinstance(user_currencies, list):  # Проверка типа
        print("Ошибка: user_currencies должен быть списком")
        user_currencies = []

    user_stocks = json_file.get("user_stocks", [])
    if not isinstance(user_stocks, list):
        print("Ошибка: user_stocks должен быть списком")
        user_stocks = []

    # Собираем всё в один словарь
    hello: str = get_time_based_greeting()
    result["greeting"] = hello
    result["cards"] = get_card_from_period(data)
    result["top_transactions"] = get_top_transactions(data)
    result["currency_rates"] = currency_rates(user_currencies)
    result["stock_prices"] = get_stock_price(user_stocks)

    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(main_page("25-11-2020 12:50:00"))
