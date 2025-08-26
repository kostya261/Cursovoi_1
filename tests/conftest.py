from datetime import datetime
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest


@pytest.fixture
def sample_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата операции": [
                datetime(2023, 1, 1),
                datetime(2023, 1, 2),
                datetime(2023, 1, 3),
                datetime(2023, 1, 1),
                datetime(2023, 1, 2),
                datetime(2023, 1, 3),
            ],
            "Категория": ["Еда", "Транспорт", "Еда", "Транспорт", "Развлечения", "Еда"],
            "Сумма операции": [100.0, 200.0, 150.0, 250.0, 300.0, 500.0],
            "Описание": ["Обед", "Такси", "Ужин", "Метро", "Кино", "Ресторан"],
        }
    )


@pytest.fixture
def sample_data_2() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Номер карты": ["1234567890123456", "9876543210987654", "1234567890123456"],
            "Сумма операции с округлением": [1000, 2000, 1500],  # Суммы для группировки
        }
    )


@pytest.fixture
def sample_data_3() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата операции": [
                "01.01.2023 10:00:00",
                "15.01.2023 12:00:00",
                "31.01.2023 23:59:59",
                "01.02.2023 00:00:00",
                "15.03.2023 15:30:00",
            ],
            "Сумма": [100, 200, 300, 400, 500],
        }
    )


@pytest.fixture
def sample_data_4() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата операции": ["01.01.2023", "15.01.2023", "31.01.2023", "01.02.2023"],
            "Категория": ["Еда", "Транспорт", "Еда", "Развлечения"],
            "Сумма": [100, 200, 150, 300],
        }
    )


@pytest.fixture
def sample_data_5() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Описание": [
                "Звоните по тел. +7 (123) 456-78-90",
                "Нет телефона в описании",
                "Мой номер: 8-900-123-45-67",
                "Ещё один контакт: 7(495)1234567",
            ],
            "Сумма": [100, 200, 300, 400],
        }
    )


@pytest.fixture
def sample_data_6() -> pd.DataFrame:
    """Фикстура с тестовыми данными, содержащими имена"""
    return pd.DataFrame(
        {
            "Описание": [
                "Клиент: Иванов И.",
                "Покупатель: Петрова А.С.",
                "Контрагент: Сидоров В.В.",
                "Без имени в описании",
                "Заказчик: Кузнецов П. (менеджер)",
            ],
            "Сумма": [100, 200, 300, 400, 500],
            "Дата операции": ["2023-01-01"] * 5,
        }
    )


@pytest.fixture
def sample_data_7() -> pd.DataFrame:
    """Фикстура с тестовыми данными для поиска"""
    return pd.DataFrame(
        {
            "Категория": ["Еда", "Транспорт", "Развлечения", "Супермаркет", "Кафе"],
            "Описание": ["Обед в кафе", "Такси до работы", "Кино", "Покупки в Пятерочке", "Кофе с коллегой"],
            "Сумма": [100, 200, 300, 400, 500],
        }
    )


@pytest.fixture
def mock_dependencies():
    """Фикстура для мокирования всех зависимостей"""
    with patch("src.loader.excel_loader") as mock_excel_loader, patch(
        "src.utils.convert_data"
    ) as mock_convert_data, patch("src.loader.load_json") as mock_load_json, patch(
        "src.utils.get_time_based_greeting"
    ) as mock_greeting, patch(
        "src.utils.get_card_from_period"
    ) as mock_cards, patch(
        "src.utils.get_top_transactions"
    ) as mock_transactions, patch(
        "src.external_api.currency_rates"
    ) as mock_currency, patch(
        "src.external_api.get_stock_price"
    ) as mock_stocks:
        # Настраиваем возвращаемые значения
        mock_convert_data.return_value = MagicMock()  # Мок DataFrame
        mock_load_json.return_value = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}
        mock_greeting.return_value = "Добрый день"
        mock_cards.return_value = [{"card": "data"}]
        mock_transactions.return_value = [{"transaction": "data"}]
        mock_currency.return_value = {"USD": 75.5, "EUR": 85.3}
        mock_stocks.return_value = {"AAPL": 150.2, "GOOGL": 2800.5}

        yield {
            "excel_loader": mock_excel_loader,
            "convert_data": mock_convert_data,
            "load_json": mock_load_json,
            "greeting": mock_greeting,
            "cards": mock_cards,
            "transactions": mock_transactions,
            "currency": mock_currency,
            "stocks": mock_stocks,
        }
