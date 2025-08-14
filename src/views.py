import json

from src.external_api import currency_rate, get_stock_price, curency_rates
from src.loader import load_json, excel_loader
from src.utils import get_time_based_greeting, get_card_from_period, get_top_transactions


def main_page(date_time: str):
    result: dict = {}

    excel_file = excel_loader("..\\data\\operations.xlsx")

    json_file = load_json("..\\user_settings.json")

    user_currencies = json_file.get("user_currencies", [])
    if not isinstance(user_currencies, list):  # Проверка типа
        print("Ошибка: user_currencies должен быть списком")
        user_currencies = []

    user_stocks = json_file.get("user_stocks", [])
    if not isinstance(user_stocks, list):
        print("Ошибка: user_stocks должен быть списком")
        user_stocks = []

    hello: str = get_time_based_greeting()
    result["greeting"] = hello
    result["cards"] = get_card_from_period(excel_file, date_time)
    result["top_transactions"] = get_top_transactions(excel_file, date_time)
    result["currency_rates"] = curency_rates(user_currencies)
    result["stock_prices"] = get_stock_price(user_stocks)

    #currency_rates = {}
    #for key_for_dict in user_currencies:
    #    currency_rates[key_for_dict] = currency_rate(key_for_dict)

    return json.dumps(result, ensure_ascii=False, indent = 2)


if __name__ == "__main__":
    print(main_page("25-11-2020 12:50:00"))
