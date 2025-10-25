"""
Здесь будет основная логика работы с таблицами и данными.
"""

import os
import json
import csv
import re

from prettytable import from_csv, PrettyTable

from src.primitive_db.constants import CONST
from src.primitive_db.utils import (
    check_table_exists,
    process_where_clause,
    get_table_columns,
)


def load_database(file_path: str) -> None:
    if not os.path.exists(file_path):
        print(f"DATABASE {file_path} не существует")
        return

    if not os.path.isfile(file_path):
        print("Это директория")
        return

    CONST.DATABASE_PATH = file_path

    with open(CONST.DATABASE_PATH, "r", encoding="utf-8") as file:
        data: dict = json.load(file)

    database_name = data.get("name")
    if database_name is None:
        print("Не определена база данных")
        return

    print(f"Используется {database_name}")


def create_database(file_path: str, database_name: str) -> None:
    if not file_path.endswith(".json"):
        file_path += ".json"

    if os.path.exists(file_path):
        if not os.path.isfile(file_path):
            print("Это директория")
            return
        print(f"DATABASE {file_path} уже существует")
        CONST.DATABASE_PATH = file_path
        return

    database = {"name": database_name, "tables": []}

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(database, file)
        CONST.DATABASE_PATH = file_path
        print(f"DATABASE {database_name} создана")


def create_table(metadata, table_name: str, table_path: str, columns: list) -> None:
    """
    1) Она должна принимать текущие метаданные, имя таблицы и список столбцов.
    2) Автоматически добавлять столбец ID:int в начало списка столбцов.
    3) Проверять, не существует ли уже таблица с таким именем. Если да, выводить ошибку.
    4) Проверять корректность типов данных (только int, str, bool).
    5) В случае успеха, обновлять словарь metadata и возвращать его.
    """

    if CONST.DATABASE_PATH is None or (
        CONST.DATABASE_PATH is not None and not os.path.exists(CONST.DATABASE_PATH)
    ):
        print(
            f"DATABASE {CONST.DATABASE_PATH} не подключена, вызовите <load_database> команду"
        )
        return

    if not os.path.isfile(CONST.DATABASE_PATH):
        print("Это директория")
        return

    with open(CONST.DATABASE_PATH, "r", encoding="utf-8") as file:
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
        if column_name == "ID":
            continue

        if column_type not in ["int", "str", "bool"]:
            print(f"Неподдерживаемый формат колонки: {column_type}")
            continue
        column = {"name": column_name, "type": column_type}
        table_columns.append(column)

    column_ID = {"name": "ID", "type": "int"}
    table_columns = [column_ID] + table_columns

    table = {"name": table_name, "path": table_path, "columns": table_columns}
    tables.append(table)
    data["tables"] = tables

    with open(CONST.DATABASE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file)

    with open(table_path, "w", encoding="utf-8") as file:
        columns_to_write = ["ID"]
        for column in table_columns:
            column_name = column["name"]
            if column_name == "ID":
                continue
            columns_to_write.append(column_name)
        string = CONST.SEPARATOR.join(columns_to_write)
        file.write(string)

    print(f"Таблица {table_name} создана")


def drop_table(metadata, table_name):
    """
    1) Проверяет существование таблицы. Если таблицы нет, выводит ошибку.
    2) Удаляет информацию о таблице из metadata и возвращает обновленный словарь.
    """

    if CONST.DATABASE_PATH is None or (
        CONST.DATABASE_PATH is not None and not os.path.exists(CONST.DATABASE_PATH)
    ):
        print(
            f"DATABASE {CONST.DATABASE_PATH} не подключена, вызовите <load_database> команду"
        )
        return

    if not os.path.isfile(CONST.DATABASE_PATH):
        print("Это директория")
        return

    with open(CONST.DATABASE_PATH, "r", encoding="utf-8") as file:
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

    with open(CONST.DATABASE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file)

    print(f"Таблица {table_name} удалена")


def list_tables(table_name: str | None = None):
    if CONST.DATABASE_PATH is None or (
        CONST.DATABASE_PATH is not None and not os.path.exists(CONST.DATABASE_PATH)
    ):
        print(
            f"DATABASE {CONST.DATABASE_PATH} не подключена, вызовите <load_database> команду"
        )
        return

    if not os.path.isfile(CONST.DATABASE_PATH):
        print("Это директория")
        return

    with open(CONST.DATABASE_PATH, "r", encoding="utf-8") as file:
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

    table_cycle_flag = True
    for table in tables:
        if not isinstance(table, dict):
            continue
        name = table.get("name")
        columns = table.get("columns")
        path = table.get("path")

        if name is None or columns is None or path is None:
            continue

        if table_name is not None and table_name == name:
            table_cycle_flag = False

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

        strings_lst = " | ".join(strings)
        print(strings_lst)
        print("-" * len(strings_lst))

        if not table_cycle_flag:
            break


def info(table_name: str) -> None:
    table_path = check_table_exists(table_name=table_name)

    if table_path is None:
        return None

    list_tables(table_name=table_name)


def select(table_name: str, where_clause: dict[str, str] | None = None) -> None:
    table_path = check_table_exists(table_name=table_name)

    if table_path is None:
        return None

    content = []
    table = PrettyTable()
    with open(table_path, "r", encoding="utf-8") as file:
        if where_clause is None:
            table = from_csv(file, delimiter=CONST.SEPARATOR)
            print(table)
            return

        reader = csv.DictReader(file, delimiter=CONST.SEPARATOR)
        keys = list(reader.__next__().keys())
        table.field_names = keys

    where_clause_processed = process_where_clause(
        table_name=table_name, where_clause=where_clause
    )
    if where_clause_processed is None:
        return None

    columns = get_table_columns(table_name=table_name)
    if columns is None:
        return None

    with open(table_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=CONST.SEPARATOR)
        for row in reader:
            flag = True
            for key, value in where_clause_processed.items():
                row_value: str | int | bool | None = None
                for column in columns:
                    if column["name"] == key:
                        t = column["type"]
                        if t == "str":
                            row_value = str(row[key])
                        elif t == "int":
                            row_value = int(row[key])
                        elif t == "bool":
                            row_value = bool(int(row[key]))
                        break

                if row_value != value:
                    flag = False
                    break
            if flag:
                values = list(row.values())
                content.append(values)

        table.add_rows(content)
        print(table)


def insert(table_name: str, values: str) -> None:
    table_path = check_table_exists(table_name=table_name)

    if table_path is None:
        return None

    values = re.sub(r"\(", "", values)
    values = re.sub(r"\)", "", values)
    values_list = values.split(", ")

    columns = get_table_columns(table_name=table_name)
    if columns is None:
        return None

    values_to_insert: list[str] = []
    columns = columns[1:]
    for column, value in zip(columns, values_list):
        t = column["type"]
        processed_value: str | None = None
        try:
            if t == "str" and re.match(r'".+"', value):
                processed_value = re.sub('"', "", value)
            elif t == "int":
                processed_value = str(int(value))
            elif t == "bool" and (value == "true" or value == "false"):
                if value == "true":
                    processed_value = str(1)
                elif value == "false":
                    processed_value = str(0)
        except Exception:
            print(f"Ошибка конвертации значения: {value} типа {t}")
            return

        if processed_value is None:
            print(f"Ошибка конвертации значения: {value} типа {t}")
            return
        values_to_insert.append(processed_value)

    with open(table_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        if len(lines) == 1:
            last_ID = 0
        else:
            last_line = lines[-1]
            last_ID = int(last_line.split(CONST.SEPARATOR)[0])
            last_ID += 1

    values_to_insert = [str(last_ID)] + values_to_insert
    string = CONST.SEPARATOR.join(values_to_insert)
    with open(table_path, "a", encoding="utf-8") as file:
        file.write("\n")
        file.write(string)

    print(f"Запись с {last_ID=} успешно добавлена в таблицу {table_name}.")


def update(
    table_name: str, set_clause, where_clause: dict[str, str] | None = None
) -> None: ...


def delete(table_name: str, where_clause: dict[str, str] | None = None) -> None:
    table_path = check_table_exists(table_name=table_name)

    if table_path is None:
        return None

    if where_clause is None:
        answer = input("Delete all records? (y/n) ")
        if answer == "y":
            with open(table_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=CONST.SEPARATOR)
                keys = CONST.SEPARATOR.join(reader.__next__())

            with open(table_path, "w", encoding="utf-8") as file:
                file.write(keys)
            print("Все записи успешно удалены")
        return

    where_clause_processed = process_where_clause(
        table_name=table_name, where_clause=where_clause
    )
    if where_clause_processed is None:
        return None

    columns = get_table_columns(table_name=table_name)
    if columns is None:
        return None

    content: list[str] = []
    values_to_delete: int = 0
    with open(table_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=CONST.SEPARATOR)
        keys = CONST.SEPARATOR.join(reader.__next__())
        content.append(keys)

    with open(table_path, "r", encoding="utf-8") as file:
        dict_reader = csv.DictReader(file, delimiter=CONST.SEPARATOR)
        for row in dict_reader:
            flag = False
            for key, value in where_clause_processed.items():
                row_value: str | int | bool | None = None
                for column in columns:
                    if column["name"] == key:
                        t = column["type"]
                        if t == "str":
                            row_value = str(row[key])
                        elif t == "int":
                            row_value = int(row[key])
                        elif t == "bool":
                            row_value = bool(int(row[key]))
                        break

                if row_value != value:
                    flag = True
                    break
            if flag:
                values = CONST.SEPARATOR.join(list(row.values()))
                content.append(values)
            else:
                values_to_delete += 1
                print(CONST.SEPARATOR.join(list(row.values())))

    with open(table_path, "w", encoding="utf-8") as file:
        content_str = "\n".join(content)
        file.write(content_str)

    print()
    print(f"{values_to_delete} записей удалены")
