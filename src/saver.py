import json


def save_json(file_path, json_data: list[dict]) -> None:
    """
    Сохраняет список в json файл
    :param file_path: - путь к файлу и имя файла
    :param json_data: список словарей для сохранения
    :return:
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)
