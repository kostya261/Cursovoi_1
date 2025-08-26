import os
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import currency_rate, get_stock_price


def test_currency_rate_success(mocker):
    """Тест успешного получения курса валют"""
    # Мокируем окружение и запрос
    mocker.patch.dict("os.environ", {"apikey": "test_api_key"})
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 75.5}
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    # Вызываем функцию
    result = currency_rate("USD")

    # Проверяем результат
    assert result == 75.5
    requests.get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "test_api_key"},
        params={"amount": 1, "from": "USD", "to": "RUB"},
        timeout=10,
    )


def test_currency_rate_no_api_key():
    """Тест отсутствия API ключа"""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ValueError, match="Отсутствует API ключ!"):
            currency_rate("EUR")


def test_currency_rate_request_error(mocker):
    """Тест ошибки запроса"""
    mocker.patch.dict("os.environ", {"apikey": "test_api_key"})
    mocker.patch("requests.get", side_effect=requests.RequestException)

    result = currency_rate("GBP")
    assert result == 0.0


def test_currency_rate_invalid_response(mocker):
    """Тест невалидного ответа API"""
    mocker.patch.dict("os.environ", {"apikey": "test_api_key"})
    mock_response = MagicMock()
    mock_response.json.return_value = {}  # Нет поля result
    mocker.patch("requests.get", return_value=mock_response)

    result = currency_rate("JPY")
    assert result == 0.0


def test_currency_rate_timeout(mocker):
    """Тест таймаута запроса"""
    mocker.patch.dict("os.environ", {"apikey": "test_api_key"})
    mocker.patch("requests.get", side_effect=requests.Timeout)

    result = currency_rate("CNY")
    assert result == 0.0


def test_currency_rate_default_currency(mocker):
    """Тест вызова с валютой по умолчанию (USD)"""
    mocker.patch.dict("os.environ", {"apikey": "test_api_key"})
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 75.5}
    mocker.patch("requests.get", return_value=mock_response)

    result = currency_rate()  # Без указания валюты
    assert result == 75.5
    requests.get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/convert",
        headers={"apikey": "test_api_key"},
        params={"amount": 1, "from": "USD", "to": "RUB"},
        timeout=10,
    )


# ______________________________________________________________________________#


def test_get_stock_price_success(mocker):
    """Тест успешного получения цен акций."""

    # Мокируем os.getenv, чтобы он возвращал фейковый API-ключ
    mocker.patch("os.getenv", return_value="Неверный API ключ")

    # Мокируем finnhub.Client и его метод quote
    mock_client = MagicMock()
    mock_client.quote.return_value = {"c": 150.0}  # Возвращаем фиктивную цену

    # Подменяем finnhub.Client на наш мок и сохраняем его вызовы
    mocked_client_class = mocker.patch("finnhub.Client", return_value=mock_client)

    # Вызываем тестируемую функцию
    tickers = ["AAPL", "GOOGL"]
    result = get_stock_price(tickers)

    # Проверяем, что os.getenv был вызван с правильным аргументом
    os.getenv.assert_called_once_with("apikey_2")

    # Проверяем, что finnhub.Client был создан с нашим API-ключом
    # Теперь используем mocked_client_class (класс), а не mock_client (экземпляр)
    assert mocked_client_class.call_args[1]["api_key"] == "Неверный API ключ"

    # Проверяем, что quote вызывался для каждого тикера
    assert mock_client.quote.call_count == len(tickers)

    # Проверяем структуру результата
    assert isinstance(result, list)
    assert len(result) == len(tickers)
    for item in result:
        assert isinstance(item, dict)
        assert any(ticker in item for ticker in tickers)


def test_get_stock_price_no_api_key(mocker):
    """Тест ошибки при отсутствии API-ключа."""

    # Мокируем os.getenv, чтобы он возвращал None (ключ отсутствует)
    mocker.patch("os.getenv", return_value=None)

    # Проверяем, что функция вызывает исключение
    with pytest.raises(ValueError, match="Отсутствует API ключ!"):
        get_stock_price(["AAPL"])


def test_get_stock_price_api_error(mocker):
    """Тест обработки ошибки API (например, если тикер не существует)."""

    mocker.patch("os.getenv", return_value="Неверный API ключ")

    mock_client = MagicMock()
    mock_client.quote.side_effect = Exception("API Error")  # Имитируем ошибку API

    mocker.patch("finnhub.Client", return_value=mock_client)

    with pytest.raises(Exception, match="API Error"):
        get_stock_price(["INVALID_TICKER"])
