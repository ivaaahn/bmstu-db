import csv
import random
import time
from datetime import datetime

import schedule

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


def generate(idx: int, count: int = 5):
    with open(gen_filename(idx), 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['full_name', 'birth_year', 'experience', 'phone'])
        writer.writeheader()

        for _ in range(count):
            empl = get_empl()
            writer.writerow(empl)

            print(empl)


def read_meta() -> int:
    return int(input("Input idx: "))


def counter_gen(num):
    while True:
        yield num
        num += 1


def main():
    counter = counter_gen(0)
    schedule.every(5).seconds.do(lambda: generate(next(counter)))

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
