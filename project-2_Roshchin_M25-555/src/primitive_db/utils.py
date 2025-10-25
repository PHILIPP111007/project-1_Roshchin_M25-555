import json


def load_metadata(file_path: str) -> None:
    """Загружает данные из JSON-файла"""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Такого файла нет.")


def save_metadata(file_path: str, data) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file)
