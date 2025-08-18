import json

import pandas as pd
import pytest

from src.services import search_line, search_name, search_phone


def test_search_phone_basic(sample_data_5):
    """Тест базового поиска телефонов"""
    result = search_phone(sample_data_5)
    data = json.loads(result)
    assert len(data) == 3  # Должно найти 3 записи с телефонами
    descriptions = [item["Описание"] for item in data]
    assert "Нет телефона в описании" not in descriptions


def test_search_phone_empty():
    """Тест с пустым DataFrame"""
    empty_df = pd.DataFrame(columns=["Описание", "Сумма"])
    with pytest.raises(ValueError, match="Передан пустой DataFrame"):
        search_phone(empty_df)


def test_search_phone_no_matches():
    """Тест без совпадений телефонов"""
    df = pd.DataFrame({"Описание": ["Нет телефона", "Тоже нет"], "Сумма": [100, 200]})
    result = search_phone(df)
    data = json.loads(result)
    assert len(data) == 0


def test_search_phone_special_cases():
    """Тест специальных форматов телефонов"""
    df = pd.DataFrame(
        {
            "Описание": ["Тел.: 8(123)4567890", "Моб.: 7 123 456 78 90", "Формат: +7-123-456-78-90"],
            "Сумма": [100, 200, 300],
        }
    )
    result = search_phone(df)
    data = json.loads(result)
    assert len(data) == 3


def test_search_phone_json_structure(sample_data_5):
    """Тест структуры возвращаемого JSON"""
    result = search_phone(sample_data_5)
    try:
        data = json.loads(result)
        assert isinstance(data, list)
        if len(data) > 0:
            assert all(isinstance(item, dict) for item in data)
            assert all("Описание" in item and "Сумма" in item for item in data)
    except json.JSONDecodeError:
        pytest.fail("Возвращаемые данные не являются валидным JSON")


def test_search_name_finds_correct_entries(sample_data_6):
    """Проверяет, что функция находит все записи с именами"""
    result = search_name(sample_data_6)
    data = json.loads(result)

    # Должно найти 4 записи с именами
    assert len(data) == 4

    # Проверяем, что записи без имён исключены
    descriptions = [item["Описание"] for item in data]
    assert "Без имени в описании" not in descriptions


def test_search_name_empty_data():
    """Проверка реакции на пустой DataFrame"""
    empty_df = pd.DataFrame(columns=["Описание", "Сумма"])
    with pytest.raises(ValueError, match="Передан пустой DataFrame"):
        search_name(empty_df)


def test_search_name_no_matches():
    """Проверка случая, когда имён нет"""
    no_names_df = pd.DataFrame({"Описание": ["Обычная транзакция", "Покупка товаров"], "Сумма": [100, 200]})
    result = search_name(no_names_df)
    assert json.loads(result) == []  # Должен вернуть пустой список


def test_search_in_category(sample_data_7):
    """Поиск по столбцу Категория"""
    # Поиск по полному совпадению
    result = search_line(sample_data_7, "Еда")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Категория"] == "Еда"

    # Поиск по части строки
    result = search_line(sample_data_7, "марк")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Категория"] == "Супермаркет"


def test_search_in_description(sample_data_7):
    """Поиск по столбцу Описание"""
    # Поиск по полному слову
    result = search_line(sample_data_7, "Такси")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Описание"] == "Такси до работы"

    # Поиск по части слова
    result = search_line(sample_data_7, "офе")
    data = json.loads(result)
    assert len(data) == 1
    assert "Кофе" in data[0]["Описание"]


def test_search_case_insensitive(sample_data_7):
    """Проверка регистронезависимости"""
    # Поиск с разным регистром
    result_upper = search_line(sample_data_7, "ЕДА")
    result_lower = search_line(sample_data_7, "еда")
    result_mixed = search_line(sample_data_7, "ЕдА")

    data_upper = json.loads(result_upper)
    data_lower = json.loads(result_lower)
    data_mixed = json.loads(result_mixed)

    assert len(data_upper) == len(data_lower) == len(data_mixed) == 1
    assert data_upper[0]["Категория"] == data_lower[0]["Категория"] == data_mixed[0]["Категория"] == "Еда"


def test_search_multiple_matches(sample_data_7):
    """Поиск с несколькими совпадениями"""
    # Слово "кафе" встречается в Категории ("Кафе") и Описании ("Обед в кафе")
    result = search_line(sample_data_7, "кафе")
    data = json.loads(result)

    # Должно найти 2 записи: "Кафе" (категория) и "Обед в кафе" (описание)
    assert len(data) == 2

    # Проверяем, что найдены обе ожидаемые записи
    categories = {item["Категория"] for item in data}
    descriptions = {item["Описание"] for item in data}
    assert "Кафе" in categories
    assert "Обед в кафе" in descriptions


def test_search_no_matches(sample_data_7):
    """Поиск без совпадений"""
    result = search_line(sample_data_7, "аптека")
    assert json.loads(result) == []


def test_search_empty_data():
    """Проверка реакции на пустой DataFrame"""
    empty_df = pd.DataFrame(columns=["Категория", "Описание"])
    with pytest.raises(ValueError, match="Передан пустой DataFrame"):
        search_line(empty_df, "test")
