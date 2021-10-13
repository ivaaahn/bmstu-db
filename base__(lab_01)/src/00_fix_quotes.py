from typing import IO


def fixer(new: IO, old: IO):
    for row in old:
        if row.count('"') == 1:
            row = row.replace('"', '')

        if row.count('""'):
            row = row.replace('""', '')

        if row.count('"') & 1:
            row = row.replace('"', '')

        new.write(row)


def main():
    with open('./data/products2.csv', 'w') as new:
        with open('./data/products.csv', 'r') as old:
            fixer(new, old)


if __name__ == '__main__':
    main()
