import json
import os

import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_basic(sample_data_4):
    """Тест базовой фильтрации по категории"""
    result = spending_by_category(sample_data_4, "Еда")
    assert len(result) == 2
    assert all(result["Категория"].str.contains("Еда", case=False))


def test_spending_by_category_empty(sample_data_4):
    """Тест с несуществующей категорией"""
    result = spending_by_category(sample_data_4, "Несуществующая")
    assert result.empty
    assert list(result.columns) == list(sample_data_4.columns)


def test_spending_by_category_with_date(sample_data_4):
    """Тест фильтрации по категории и дате"""
    result = spending_by_category(sample_data_4, "Еда", start_date="15.01.2023")
    assert len(result) == 1
    assert result.iloc[0]["Категория"] == "Еда"


def test_save_to_json(tmp_path, sample_data_4):
    """Тест сохранения в JSON"""
    filename = tmp_path / "test.json"
    spending_by_category(sample_data_4, "Еда", filename=str(filename))

    assert os.path.exists(filename)
    with open(filename, "r") as f:
        data = json.load(f)
    assert len(data) == 2


def test_save_to_csv(tmp_path, sample_data_4):
    """Тест сохранения в CSV"""
    filename = tmp_path / "test.csv"
    spending_by_category(sample_data_4, "Еда", filename=str(filename))

    assert os.path.exists(filename)
    df = pd.read_csv(filename)
    assert len(df) == 2


def test_save_to_excel(tmp_path, sample_data_4):
    """Тест сохранения в Excel"""
    filename = tmp_path / "test.xlsx"
    spending_by_category(sample_data_4, "Еда", filename=str(filename))

    assert os.path.exists(filename)
    df = pd.read_excel(filename)
    assert len(df) == 2


def test_save_default_format(tmp_path, sample_data_4):
    """Тест сохранения с форматом по умолчанию"""
    filename = tmp_path / "test"  # Без расширения
    spending_by_category(sample_data_4, "Еда", filename=str(filename))

    assert os.path.exists(str(filename) + ".json")


def test_error_handling(sample_data_4, capsys):
    """Тест обработки ошибок"""
    # Создаем невалидные данные
    invalid_data = sample_data_4.copy()
    invalid_data["Дата операции"] = "invalid_date"

    result = spending_by_category(invalid_data, "Еда")
    assert result.empty
    assert "Ошибка при фильтрации" in capsys.readouterr().out
