import csv
import random
from datetime import datetime

TABLE = 'employee'

NAMES = [
    'Anton',
    'Vasya',
    'Dima',
    'Petya',
    'Oleg',
    'Petr',
    'Evgeny'
]

PHONE = '+79'


def get_empl() -> dict:
    return {
        'full_name': random.choice(NAMES),
        'birth_year': random.randint(1970, 2002),
        'experience': random.randint(1, 5),
        'phone': PHONE + str(random.randint(100000000, 999999999))
    }


def gen_filename(idx: int) -> str:
    return f'input/{idx}_{TABLE}_{datetime.now()}.csv'


def generate(idx: int):
    empl = get_empl()
    with open(gen_filename(idx), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['full_name', 'birth_year', 'experience', 'phone'])
        writer.writeheader()
        writer.writerow(empl)

        print(empl)


def read_meta() -> int:
    return int(input("Input idx: "))


def main():
    generate(read_meta())


if __name__ == '__main__':
    main()
