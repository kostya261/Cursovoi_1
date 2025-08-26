import json
from unittest.mock import MagicMock, patch


@patch("src.views.excel_loader")
@patch("src.views.convert_data")
@patch("src.views.load_json")
@patch("src.views.get_time_based_greeting")
@patch("src.views.get_card_from_period")
@patch("src.views.get_top_transactions")
@patch("src.views.currency_rates")
@patch("src.views.get_stock_price")
def test_main_page_success(
    mock_stock, mock_rates, mock_top, mock_cards, mock_greet, mock_json, mock_convert, mock_excel
):
    """Тест успешного выполнения с полной изоляцией"""

    mock_excel.return_value = "fake_excel"
    mock_convert.return_value = MagicMock()  # любой непустой объект
    mock_json.return_value = {"user_currencies": ["USD"], "user_stocks": ["AAPL"]}
    mock_greet.return_value = "Привет"
    mock_cards.return_value = {"cards": "test"}
    mock_top.return_value = {"top": "transactions"}
    mock_rates.return_value = {"USD": 75.0}
    mock_stock.return_value = [{"AAPL": 150.0}]

    from src.views import main_page

    result = json.loads(main_page("01-01-2021 00:00:00"))

    assert result == {
        "greeting": "Привет",
        "cards": {"cards": "test"},
        "top_transactions": {"top": "transactions"},
        "currency_rates": {"USD": 75.0},
        "stock_prices": [{"AAPL": 150.0}],
    }

    mock_convert.assert_called_once_with("fake_excel", "01-01-2021 00:00:00")


# Тест для невалидных user_currencies
@patch("src.views.excel_loader")
@patch("src.views.convert_data")
@patch("src.views.load_json")
@patch("src.views.get_time_based_greeting")
@patch("src.views.get_card_from_period")
@patch("src.views.get_top_transactions")
@patch("src.views.currency_rates")
@patch("src.views.get_stock_price")
def test_main_page_invalid_user_currencies(
    mock_stock, mock_rates, mock_top, mock_cards, mock_greet, mock_json, mock_convert, mock_excel, capsys
):
    """Тест обработки невалидных user_currencies"""

    mock_excel.return_value = MagicMock()
    mock_convert.return_value = MagicMock()
    mock_json.return_value = {"user_currencies": "not_a_list"}  # Неправильный тип
    mock_greet.return_value = "Привет"
    mock_cards.return_value = {}
    mock_top.return_value = {}
    mock_rates.return_value = {}  # Пустой словарь для валют
    mock_stock.return_value = []  # Пустой список для акций

    from src.views import main_page

    result = json.loads(main_page("01-01-2021 00:00:00"))
    captured = capsys.readouterr()

    assert "Ошибка: user_currencies должен быть списком" in captured.out
    assert result["currency_rates"] == {}
    assert result["stock_prices"] == []


# Тест для пустых данных
@patch("src.views.excel_loader")
@patch("src.views.convert_data")
@patch("src.views.load_json")
@patch("src.views.get_time_based_greeting")
@patch("src.views.get_card_from_period")
@patch("src.views.get_top_transactions")
@patch("src.views.currency_rates")
@patch("src.views.get_stock_price")
def test_main_page_empty_data(
    mock_stock, mock_rates, mock_top, mock_cards, mock_greet, mock_json, mock_convert, mock_excel
):
    """Тест работы с пустыми данными"""

    mock_excel.return_value = MagicMock()
    mock_convert.return_value = {}
    mock_json.return_value = {}
    mock_greet.return_value = "Привет"
    mock_cards.return_value = {}
    mock_top.return_value = {}
    mock_rates.return_value = {}
    mock_stock.return_value = []

    from src.views import main_page

    result = json.loads(main_page("01-01-2021 00:00:00"))
    assert result == {
        "greeting": "Привет",
        "cards": {},
        "top_transactions": {},
        "currency_rates": {},
        "stock_prices": [],
    }
