from labyrinth_game.types import GAME_STATE, ROOM
from labyrinth_game.constants import ROOMS


def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")


def describe_current_room(game_state: GAME_STATE):
    current_room: ROOM = ROOMS[game_state["current_room"]]

    if current_room["items"]:
        items = "Заметные предметы: "
        items += ", ".join(current_room["items"])
    else:
        items = ""

    exits = current_room["exits"]
    exits_str = "Выходы:\n"
    for direction, room in exits.items():
        exits_str += f"{direction} -> {room}\n"

    puzzle = current_room["puzzle"]
    puzzle_str = ""
    if puzzle is not None:
        puzzle_str += puzzle[0]

    print(f"== {game_state['current_room']} ==")
    print(f"== {current_room['description']} ==")
    if items:
        print(items)

    print(exits_str)

    if puzzle_str:
        print(puzzle_str)


def solve_puzzles(game_state: GAME_STATE) -> GAME_STATE | None:
    current_room: ROOM = ROOMS[game_state["current_room"]]

    if current_room["puzzle"] is None:
        print("Загадок здесь нет.")
        return

    puzzle = current_room["puzzle"][0]
    correct_answer = current_room["puzzle"][1]
    print(puzzle)

    user_answer = input("Ваш ответ: ")

    if user_answer == correct_answer:
        print("Вы разгадали загадку!")
        current_room["puzzle"] = None

        game_state["rewards"] += 1

        if game_state["current_room"] == "treasure_room":
            game_state["game_over"] = True
            current_room["items"].remove("treasure chest")
            print("Вы прошли игру!")
        ROOMS[game_state["current_room"]] = current_room
    else:
        print("Неверно, попробуйте еще снова.")

    return game_state


def attempt_open_treasure(game_state: GAME_STATE) -> GAME_STATE:
    current_room: ROOM = ROOMS[game_state["current_room"]]
    items = current_room["items"]
    user_items = game_state["player_inventory"]

    if "treasure chest" in items:
        if "treasure_key" in user_items or "rusty_key" in user_items:
            print("Вы применяете ключ, и замок щелкает. Сундук открыт!")

            current_room["items"].remove("treasure chest")
            if "treasure_key" in user_items:
                user_items.remove("treasure_key")
            elif "rusty_key" in user_items:
                user_items.remove("rusty_key")

            game_state["game_over"] = True
            game_state["player_inventory"] = user_items
            print("Вы прошли игру!")
        else:
            print("У вас нет ключей.")
            answer = input("Сундук заперт. ... Ввести код (да/нет)")
            if answer == "да":
                solve_puzzles(game_state=game_state)
            else:
                print("Вы отступаете от сундука.")
    else:
        print("Сундук уже открыт или отсутствует.")

    return game_state
