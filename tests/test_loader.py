import json
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.loader import excel_loader, load_json


def test_excel_loader_success(tmp_path):
    """Тест успешной загрузки Excel-файла."""

    # Создаем временный Excel-файл для теста
    test_data = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    test_file = tmp_path / "test.xlsx"
    test_data.to_excel(test_file, index=False)

    # Вызываем функцию и проверяем результат
    result = excel_loader(str(test_file))

    # Проверяем, что возвращается DataFrame и данные корректны
    assert isinstance(result, pd.DataFrame)
    assert result.equals(test_data)


def test_excel_loader_file_not_found():
    """Тест ошибки, если файл не существует."""

    with pytest.raises(ValueError, match="Ошибка!"):
        excel_loader("non_existent_file.xlsx")


@patch("pandas.read_excel")
def test_excel_loader_invalid_format(mock_read_excel):
    """Тест ошибки, если файл не в XLSX-формате."""

    # Имитируем ошибку парсинга
    mock_read_excel.side_effect = pd.errors.ParserError("Invalid format")

    with pytest.raises(ValueError, match="Неверный XLSX формат"):
        excel_loader("invalid_file.xlsx")


def test_load_json_success(tmp_path):
    """Тест успешной загрузки JSON-файла."""

    # Создаем временный JSON-файл
    test_data = {"key": "value"}
    test_file = tmp_path / "test.json"
    test_file.write_text(json.dumps(test_data), encoding="utf-8")

    # Проверяем, что функция возвращает правильный словарь
    result = load_json(str(test_file))
    assert result == test_data


def test_load_json_file_not_found():
    """Тест случая, когда файл не существует."""

    result = load_json("non_existent_file.json")
    assert result == {}


def test_load_json_empty_file(tmp_path):
    """Тест случая, когда файл пуст."""

    test_file = tmp_path / "empty.json"
    test_file.write_text("", encoding="utf-8")

    result = load_json(str(test_file))
    assert result == {}


def test_load_json_invalid_json(tmp_path):
    """Тест случая, когда файл содержит некорректный JSON."""

    test_file = tmp_path / "invalid.json"
    test_file.write_text("{invalid json}", encoding="utf-8")

    result = load_json(str(test_file))
    assert result == {}


def test_load_json_debug_mode(capsys, monkeypatch):
    """Тест вывода отладочных сообщений."""
    test_data = {"key": "value"}

    # Создаем мок для Path.open
    mock_file = mock_open(read_data=json.dumps(test_data))

    # Мокируем все необходимые методы Path
    def mock_is_file(self):
        return True

    monkeypatch.setattr("pathlib.Path.is_file", mock_is_file)
    monkeypatch.setattr("pathlib.Path.open", mock_file)

    # Проверяем вывод при успешной загрузке
    result = load_json("test.json", debug=True)
    captured = capsys.readouterr()
    assert "load_json - Ok!" in captured.out
    assert result == test_data

    # Проверяем вывод при отсутствии файла
    def mock_is_file_false(self):
        return False

    monkeypatch.setattr("pathlib.Path.is_file", mock_is_file_false)
    result = load_json("missing.json", debug=True)
    captured = capsys.readouterr()
    assert "load_json - нет имени файла!" in captured.out
    assert result == {}
