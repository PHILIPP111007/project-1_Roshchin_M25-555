"""
Здесь будет основная логика работы с таблицами и данными.
"""

import os
import json

DATABASE_PATH = None


def load_database(file_path: str) -> None:
    global DATABASE_PATH

    if not os.path.exists(file_path):
        print(f"DATABASE {file_path} не существует")
        return

    if not os.path.isfile(file_path):
        print("Это директория")
        return

    DATABASE_PATH = file_path

    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    database_name = data.get("name")
    if database_name is None:
        print("Не определена база данных")
        return

    print(f"Используется {database_name}")


def create_database(file_path: str, database_name: str) -> None:
    global DATABASE_PATH

    if os.path.exists(file_path):
        if not os.path.isfile(file_path):
            print("Это директория")
            return
        print(f"DATABASE {file_path} уже существует")
        DATABASE_PATH = file_path
        return

    database = {"name": database_name, "tables": []}

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(database, file)
        DATABASE_PATH = file_path
        print(f"DATABASE {database_name} создана")


def create_table(metadata, table_name: str, table_path: str, columns: list) -> None:
    """
    1) Она должна принимать текущие метаданные, имя таблицы и список столбцов.
    2) Автоматически добавлять столбец ID:int в начало списка столбцов.
    3) Проверять, не существует ли уже таблица с таким именем. Если да, выводить ошибку.
    4) Проверять корректность типов данных (только int, str, bool).
    5) В случае успеха, обновлять словарь metadata и возвращать его.
    """

    if DATABASE_PATH is None or (
        DATABASE_PATH is not None and not os.path.exists(DATABASE_PATH)
    ):
        print(
            f"DATABASE {DATABASE_PATH} не подключена, вызовите <load_database> команду"
        )
        return

    if not os.path.isfile(DATABASE_PATH):
        print("Это директория")
        return

    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    database_name = data.get("name")
    if database_name is None:
        print("Не определена база данных")
        return

    tables = data.get("tables")
    if not isinstance(tables, list):
        print("Данные повреждены")
        return

    table_flag = True
    for table in tables:
        if not isinstance(table, dict):
            continue
        name = table.get("name")
        if name == table_name:
            print(f"Таблица {table_name} уже создана")
            table_flag = False
            break

    if not table_flag:
        return

    if os.path.exists(table_path):
        print(f"Таблица по пути {table_path} уже существует")
        return

    table_columns = []
    for column in columns:
        column_name, column_type = column.split(":")
        if column_type not in ["int", "str", "bool"]:
            print(f"Неподдерживаемый формат колонки: {column_type}")
            continue
        column = {"name": column_name, "type": column_type}
        table_columns.append(column)

    table = {"name": table_name, "path": table_path, "columns": table_columns}
    tables.append(table)
    data["tables"] = tables

    with open(DATABASE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file)

    with open(table_path, "w", encoding="utf-8") as file:
        columns_to_write = []
        for column in table_columns:
            column_name = column["name"]
            columns_to_write.append(column_name)
        string = "\t".join(columns_to_write)
        file.write(string)

    print(f"Таблица {table_name} создана")


def drop_table(metadata, table_name):
    """
    1) Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    2) Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    """

    if DATABASE_PATH is None or (
        DATABASE_PATH is not None and not os.path.exists(DATABASE_PATH)
    ):
        print(
            f"DATABASE {DATABASE_PATH} не подключена, вызовите <load_database> команду"
        )
        return

    if not os.path.isfile(DATABASE_PATH):
        print("Это директория")
        return

    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    database_name = data.get("name")
    if database_name is None:
        print("Не определена база данных")
        return

    tables = data.get("tables")
    if not isinstance(tables, list):
        print("Данные повреждены")
        return

    table_flag = False
    for table in tables:
        if not isinstance(table, dict):
            continue
        name = table.get("name")
        if name == table_name:
            table_flag = True
            path = table.get("path")
            if not os.path.exists(path):
                print("Не удалось найти путь к таблице")
                return
            else:
                os.remove(path)
            break

    if not table_flag:
        print(f"Не удалось удалить таблицу {table_name}")
        return

    tables = list(filter(lambda table: table["name"] != table_name, tables))
    data["tables"] = tables

    with open(DATABASE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file)

    print(f"Таблица {table_name} удалена")


def list_tables():
    if not os.path.exists(DATABASE_PATH):
        print(
            f"DATABASE {DATABASE_PATH} не подключена, вызовите <load_database> команду"
        )
        return

    if not os.path.isfile(DATABASE_PATH):
        print("Это директория")
        return

    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    database_name = data.get("name")
    if database_name is None:
        print("Не определена база данных")
        return

    tables = data.get("tables")
    if not isinstance(tables, list):
        print("Данные повреждены")
        return
    print()

    for table in tables:
        if not isinstance(table, dict):
            continue
        name = table.get("name")
        columns = table.get("columns")
        path = table.get("path")

        if name is None or columns is None or path is None:
            continue

        print(f"Table: {name}")
        print(f"Table path: {path}")
        print("Columns:")

        strings = []
        for column in columns:
            column_name = column.get("name")
            column_type = column.get("type")

            if column_name is None or column_type is None:
                continue

            strings.append(f"{column_name} : {column_type}")

        strings = " | ".join(strings)
        print(strings)
        print("-" * len(strings))
