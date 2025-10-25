import sys

from src.primitive_db.core import (
    DATABASE_PATH,
    create_table,
    drop_table,
    list_tables,
    create_database,
    load_database,
)


def run():
    """
    В цикле:
    1) Загружайте актуальные метаданные с помощью load_metadata.
    2) Запрашивайте ввод у пользователя.
    3) Разбирайте введенную строку на команду и аргументы.
    4) После каждой успешной операции (create_table, drop_table) сохраняйте
    измененные метаданные с помощью save_metadata.
    """

    help_string = """
***База данных***

Функции:
* <command> load_database <file_path> -  подключить базу данных
* <command> create_database <имя_базы_данных> <file_path> - создать базу данных
* <command> create_table <имя_таблицы> <table_path> <столбец1:тип> <столбец2:тип> .. - создать таблицу
* <command> list_tables - показать список всех таблиц
* <command> drop_table <имя_таблицы> - удалить таблицу
* <command> exit - выход из программы
* <command> help - справочная информация
"""

    print(help_string)

    while True:
        try:
            args = input("Введите команду: ")
            args = args.split(" ")

            if len(args) == 0:
                print("Введите комманду!")
                continue

            command = args[0]

            if command == "help":
                print(help_string)
            elif command == "exit":
                sys.exit(0)
            elif command == "load_database":
                if len(args) < 2:
                    print("Не приведены данные")
                    continue

                file_path = args[1]
                load_database(file_path=file_path)
            elif command == "create_database":
                if len(args) < 3:
                    print("Не приведены данные")
                    continue

                database_name = args[1]
                file_path = args[2]
                create_database(file_path=file_path, database_name=database_name)
            elif command == "list_tables":
                list_tables()
            elif command == "create_table":
                if len(args) < 3:
                    print("Не приведены данные")
                    continue

                table_name = args[1]
                table_path = args[2]
                columns = args[3:]
                metadata = {}  # TODO
                create_table(
                    metadata=metadata,
                    table_name=table_name,
                    table_path=table_path,
                    columns=columns,
                )
            elif command == "drop_table":
                if len(args) < 2:
                    print("Не приведены данные")
                    continue

                table_name = args[1]
                metadata = {}  # TODO
                drop_table(metadata=metadata, table_name=table_name)
            else:
                print(f"Функции <{command}> нет. Попробуйте снова.")
        except KeyboardInterrupt:
            sys.exit(0)
