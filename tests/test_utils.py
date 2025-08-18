from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd
import pytest
from dateutil.relativedelta import relativedelta

from src.utils import (extract_name_parts, extract_phones, filter_by_date, get_card_from_period,
                       get_time_based_greeting, get_top_transactions)


@pytest.mark.parametrize(
    "hour, expected_greeting",
    [
        (4, "Доброй ночи"),
        (5, "Доброе утро"),
        (11, "Доброе утро"),
        (12, "Добрый день"),
        (16, "Добрый день"),
        (17, "Добрый вечер"),
        (22, "Добрый вечер"),
        (23, "Доброй ночи"),
    ],
)
def test_get_time_based_greeting(hour, expected_greeting):
    """Тестируем приветствие в зависимости от времени."""
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value.hour = hour
        assert get_time_based_greeting() == expected_greeting


def test_default_end_date():
    """Тестируем дефолтное значение конечной даты"""
    df = pd.DataFrame(
        {"Дата операции": ["01.01.2023", "01.04.2023", "15.04.2023", "30.06.2023"], "Сумма": [100, 200, 300, 400]}
    )

    result = filter_by_date(df, start_date="01.01.2023")

    assert len(result) == 2
    assert pd.to_datetime("01.01.2023", dayfirst=True) in result["Дата операции"].values
    assert pd.to_datetime("01.04.2023", dayfirst=True) in result["Дата операции"].values
    assert pd.to_datetime("15.04.2023", dayfirst=True) not in result["Дата операции"].values


def test_default_both_dates():
    """Тестируем дефолтные значения"""
    df = pd.DataFrame(
        {
            "Дата операции": [
                (datetime.now() - timedelta(days=10)).strftime("%d.%m.%Y"),
                (datetime.now() + timedelta(days=10)).strftime("%d.%m.%Y"),
                (datetime.now() + relativedelta(months=4)).strftime("%d.%m.%Y"),
            ],
            "Сумма": [100, 200, 300],
        }
    )

    result = filter_by_date(df)
    assert len(result) == 2


def test_filter_empty_data():
    empty_df = pd.DataFrame(columns=["Дата операции", "Сумма"])
    with pytest.raises(ValueError, match="Передан пустой DataFrame"):
        filter_by_date(empty_df)


def test_filter_invalid_dates(sample_data_3):
    """Тестируем неправильные даты"""
    with pytest.raises(ValueError):
        filter_by_date(sample_data_3, "invalid_date", "31.01.2023")
    with pytest.raises(ValueError):
        filter_by_date(sample_data_3, "01.01.2023", "invalid_date")


def test_default_date_range(sample_data_3):
    result = filter_by_date(sample_data_3)
    assert len(result) > 0


@pytest.mark.parametrize(
    "test_case, expected_results, should_raise",
    [
        (
            "basic_case",
            [
                {"last_digits": "234567890123456", "total_spent": 2500, "cashback": 25.0},
                {"last_digits": "876543210987654", "total_spent": 2000, "cashback": 20.0},
            ],
            False,
        ),
        ("empty_data", [], True),
        ("single_card", [{"last_digits": "4567890123456789", "total_spent": 5000, "cashback": 50.0}], False),
    ],
)
def test_get_card_from_period(test_case, expected_results, should_raise):
    """Тест функции которая берет карты за указанный период"""
    if test_case == "basic_case":
        df = pd.DataFrame(
            {
                "Номер карты": ["1234567890123456", "9876543210987654", "1234567890123456"],
                "Сумма операции с округлением": [1000, 2000, 1500],
            }
        )
    elif test_case == "empty_data":
        df = pd.DataFrame(columns=["Номер карты", "Сумма операции с округлением"])
    elif test_case == "single_card":
        df = pd.DataFrame(
            {
                "Номер карты": ["54567890123456789"],
                "Сумма операции с округлением": [5000],
            }
        )

    if should_raise:
        with pytest.raises(ValueError, match="Передан пустой DataFrame"):
            get_card_from_period(df)
    else:
        result = get_card_from_period(df)
        assert len(result) == len(expected_results)

        if expected_results:
            result_sorted = sorted(result, key=lambda x: x["last_digits"])
            expected_sorted = sorted(expected_results, key=lambda x: x["last_digits"])

            for res, exp in zip(result_sorted, expected_sorted):
                assert res["last_digits"] == exp["last_digits"]
                assert res["total_spent"] == exp["total_spent"]
                assert res["cashback"] == exp["cashback"]


@pytest.mark.parametrize(
    "test_case, expected_categories, expected_len",
    [
        ("default", ["Еда", "Транспорт", "Развлечения"], 3),
        ("many_categories", ["Категория_" + str(i) for i in range(10)], 10),
        ("empty_data", [], 0),
    ],
)
def test_get_top_transactions_parametrized(test_case, expected_categories, expected_len, sample_data):
    """Тестируем функцию извлекающую ТОП 10 транзакций"""
    if test_case == "default":
        df = sample_data
    elif test_case == "many_categories":
        data = {
            "Дата операции": [datetime(2023, 1, 1)] * 15,
            "Категория": ["Категория_" + str(i) for i in range(15)],
            "Сумма операции": [100.0] * 15,
            "Описание": ["Описание"] * 15,
        }
        df = pd.DataFrame(data)
    elif test_case == "empty_data":
        df = pd.DataFrame(columns=["Дата операции", "Категория", "Сумма операции", "Описание"])

    result = get_top_transactions(df)

    assert len(result) == expected_len

    if expected_len > 0:
        result_categories = [item["category"] for item in result]
        assert result_categories == expected_categories

        for item in result:
            assert all(key in item for key in ["date", "amount", "category", "description"])
            assert isinstance(item["amount"], float)
            datetime.strptime(item["date"], "%d.%m.%Y")


def test_get_top_transactions_empty_dataframe():

    empty_df = pd.DataFrame(columns=["Дата операции", "Категория", "Сумма операции", "Описание"])
    assert get_top_transactions(empty_df) == []


def test_extract_name_parts():
    """Тестируем функцию извлекающую Имена"""

    assert extract_name_parts("Иван П.") == ["Иван П."]
    assert extract_name_parts("Anna K") == ["Anna K"]
    assert extract_name_parts("Алексей С") == ["Алексей С"]

    text = "Студенты: Иван П., Anna K, ошибка: иван П."
    assert extract_name_parts(text) == ["Иван П.", "Anna K"]

    assert extract_name_parts("иван П.") == []
    assert extract_name_parts("Иванп.") == []
    assert extract_name_parts("Иван п.") == []


def test_extract_phones():
    """Тестируем функцию извлекающую номера телефонов"""
    assert extract_phones("+7 (123) 456-78-90") == ["+7 (123) 456-78-90"]
    assert extract_phones("8(123)4567890") == ["8(123)4567890"]
    assert extract_phones("71234567890") == ["71234567890"]

    assert extract_phones("+7 123 456 78 90") == ["+7 123 456 78 90"]
    assert extract_phones("8-123-456-78-90") == ["8-123-456-78-90"]

    assert extract_phones("1234567890") == []
    assert extract_phones("+7 (123) 456-78") == []

    text = "Звоните: +7 (111) 222-33-44 или 8 (222) 333-44-55"
    assert extract_phones(text) == ["+7 (111) 222-33-44", "8 (222) 333-44-55"]

    assert extract_phones("") == []
