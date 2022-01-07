from tabulate import tabulate

from queries import (
    LINQ_TO_OBJECT_DESCR as ltoobj,
    LINQ_TO_JSON_DESCR as ltojson,
    LINQ_TO_SQL_DESCR as ltosql
)


def print_table(table):
    print(tabulate(table[1], headers=[desc for desc in table[0]], tablefmt="psql"))


def print_menu():
    for key, value in ltoobj.items():
        print(f'{key}. {value[0]}')

    print()

    for key, value in ltojson.items():
        print(f'{key}. {value[0]}')

    print()

    for key, value in ltosql.items():
        print(f'{key}. {value[0]}')

    print('\n')
