import os
from typing import Any

import finnhub
import requests
from dotenv import load_dotenv

load_dotenv()


def currency_rate(currency: str = "USD") -> float | Any:
    """
    Выясняет курс валюты

    :param currency: - вид валюты
    :return: - сумма в рублях
    """

    # Проверка API ключа
    api_key = os.getenv("apikey")
    if not api_key:
        raise ValueError("Отсутствует API ключ!")

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": api_key}
    params = {"amount": 1, "from": currency, "to": "RUB"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Проверка HTTP ошибок
        return round(response.json()["result"], 2)
    except (requests.RequestException, KeyError, ValueError):
        return 0.0  # Возвращаем 0 при ошибке конвертации


def get_stock_price(tickers: list) -> list[dict]:
    """
    Возвращает текущую цену акций по тикеру.
    :params tickers: - Список фирм, по которым нужно получить актуальную цену акции
    :return: - возвращает словарь с ключом в виде наименования фирмы и значение цена акции
    """

    api_key2 = os.getenv("apikey_2")

    if not api_key2:
        raise ValueError("Отсутствует API ключ!")
    finnhub_client = finnhub.Client(api_key=api_key2)

    result: dict = {}
    temp: list = []
    for ticker in tickers:
        quote_result = finnhub_client.quote(ticker)["c"]
        result[ticker] = quote_result
        temp.append(result)

    return temp


def currency_rates(currencys: list) -> list:
    """
    Данная функция принимает на вход список валют и поочереди получает по ним данные
    через API
    :param currencys: - список валют
    :return: - список с результатами полученными через API
    """
    result: list[dict] = []
    temp: dict = {}
    for item in currencys:
        temp[item] = currency_rate(item)

    result.append(temp)

    return result
