import asyncio
from dataclasses import dataclass
from random import uniform

import aiohttp
from bs4 import BeautifulSoup as bs

FILE_TO_PARSE = 'data/delivery_restaurants_2.html'
FILE_TO_SAVE_PROD = 'data/products.csv'
FILE_TO_SAVE_REST = 'data/restaurants.csv'

R_INDEX = 1
P_INDEX = 1


@dataclass
class Restaurant:
    id: int
    reference: str
    rating: float
    name: str


@dataclass
class Product:
    id: int
    name: str
    price: float
    rest_id: int


RESTAURANTS: dict[str, Restaurant] = {}
PRODUCTS: dict[int, dict[str, Product]] = {}


async def fetch_html(client, ref):
    async with client.get(ref) as resp:
        return await resp.text()


async def parse_products(client, rest: Restaurant) -> int:
    global P_INDEX

    name_class = 'menu-product__title'
    price_class = 'menu-product__price'

    html = await fetch_html(client, rest.reference)
    soup = bs(html, 'lxml')

    raw_names, raw_prices = soup.find_all(class_=name_class), soup.find_all(class_=price_class)
    for raw_name, raw_price in zip(raw_names, raw_prices):
        name, price = raw_name.text.strip(), int(raw_price.text.strip().split()[0])

        try:
            PRODUCTS[rest.id][name]
            continue
        except KeyError:
            pass

        if rest.id not in PRODUCTS:
            PRODUCTS[rest.id] = {name: Product(price=price, name=name, rest_id=rest.id, id=P_INDEX)}
        else:
            PRODUCTS[rest.id][name] = Product(price=price, name=name, rest_id=rest.id, id=P_INDEX)

        P_INDEX += 1

    return len(PRODUCTS[rest.id]) if PRODUCTS.get(rest.id) is not None else 0


async def parse_restaurants():
    global R_INDEX
    title_class = 'vendor-item__title-text'
    link_class = 'vendor-item__link'
    with open(FILE_TO_PARSE, "r") as f:
        soup = bs(f, 'lxml')

        for ref in soup.find_all(class_=link_class):
            name = ref.find(class_=title_class).text

            if name not in RESTAURANTS:
                RESTAURANTS[name] = Restaurant(id=R_INDEX,
                                               reference='https://www.delivery-club.ru/' + ref["href"],
                                               name=name,
                                               rating=round(uniform(1, 4.9), 1))
                R_INDEX += 1


async def parse_menu():
    async with aiohttp.ClientSession() as client:
        bad = []

        for rest in sorted(RESTAURANTS.values(), key=lambda x: x.id):
            print(rest, end='')

            i = 5
            num_of_new_products = 0
            while i > 0 and not num_of_new_products:
                if i != 5:
                    print(f"({5 - i}) TRY AGAIN!!!")

                num_of_new_products = await parse_products(client, rest)
                i -= 1

            if i == 4:
                print(": DONE!!!")
            elif num_of_new_products:
                print("UHHH DONE!!!")
            else:
                print("NOPE")
                bad.append(rest.name)

        print("К хуям удаляю: ")
        for name in bad:
            print(RESTAURANTS.pop(name))


def write_restaurants():
    v = sorted(RESTAURANTS.values(), key=lambda x: x.id)
    with open(FILE_TO_SAVE_REST, "w") as f:
        for rest in v:
            string = f'{rest.id};{rest.name};{rest.rating}\n'
            f.write(string)


def write_products():
    rests = PRODUCTS.values()
    with open(FILE_TO_SAVE_PROD, "w") as f:
        for rest in rests:
            for prod in rest.values():
                string = f'{prod.id};{prod.name};{prod.price};{prod.rest_id}\n'
                f.write(string)


async def main():
    await parse_restaurants()
    await parse_menu()
    write_restaurants()
    write_products()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
