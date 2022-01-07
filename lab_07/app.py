from typing import Optional

from queries import (
    LINQ_TO_OBJECT_QUERIES as ltoobj,
    LINQ_TO_JSON_QUERIES as ltojson,
    LINQ_TO_SQL_QUERIES as ltosql
)

from utils import (
    print_menu,
    print_table
)


def get_choice() -> Optional[int]:
    try:
        choice = int(input("Input option: "))
    except ValueError:
        choice = None

    return choice


def handle_choice(choice: Optional[int]) -> bool:
    if choice is None:
        print("Bad choice")
    elif choice in (1, 2, 3, 4, 5):
        print_table(ltoobj[choice])
    elif choice == 6:
        print_table(ltojson[choice])
    elif choice in (7, 8):
        ltojson[choice].execute()
    elif choice in (9, 10):
        print_table(ltosql[choice])
    elif choice in (11, 12, 13):
        ltosql[choice].execute()
    elif choice == 14:
        ltosql[choice]()
    elif choice == 0:
        print("Exiting...")
        return False
    else:
        print('Bad choice!')

    return True


def go():
    while True:
        print_menu()

        if not handle_choice(get_choice()):
            return


if __name__ == "__main__":
    try:
        go()
    except Exception as e:
        print(f'Что-то пошло не так...\n{e}')
