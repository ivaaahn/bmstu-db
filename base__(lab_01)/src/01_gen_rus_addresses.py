import csv
import random
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

CITIES: list[str] = []
STREETS: list[str] = []


@dataclass
class Restaurant:
    id: int
    name: str
    rating: float


@dataclass
class Customer:
    id: int
    first_name: str
    last_name: Optional[str]
    birthdate: Optional[date]
    email: Optional[str]
    phone_number: str
    registered_at: datetime


RESTAURANTS: list[Restaurant] = []
CUSTOMERS: list[Customer] = []

REST_ADDR: dict[Restaurant, list[int]] = {r: [] for r in RESTAURANTS}


@dataclass
class RestAddress:
    id: int
    city: str
    street: str
    house: int
    restaurant_id: int


@dataclass
class CustomerAddress:
    id: int
    city: str
    street: str
    house: int
    entrance: int
    floor: int
    flat: int
    customer_id: int


CUSTOMER_ADDRESSES: list[CustomerAddress] = []
REST_ADDRESSES: list[RestAddress] = []


def load_restaurants() -> None:
    global RESTAURANTS
    with open('../data/restaurants.csv', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        RESTAURANTS = [
            Restaurant(
                id=int(row[0]),
                name=row[1],
                rating=float(row[2]),
            ) for row in reader]


def load_customers() -> None:
    global CUSTOMERS
    with open('../data/customers.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        CUSTOMERS = [
            Customer(
                id=int(row[0]),
                first_name=row[1],
                last_name=row[2] if row[2] else None,
                birthdate=datetime.strptime(row[3], "%Y-%m-%d") if row[3] else None,
                email=row[4] if row[4] else None,
                phone_number=row[5],
                registered_at=datetime.strptime(row[6], "%Y-%m-%d %H:%M:%S"),
            ) for row in reader]


def load_cities() -> None:
    global CITIES
    with open('../data/cities_russia.txt', 'r', newline='') as f:
        for city in f:
            CITIES.append(city[:-1])


def load_streets() -> None:
    global STREETS
    with open('../data/streets_russia.txt', 'r', newline='') as f:
        for street in f:
            STREETS.append(street[:-1])


def load_customer_addresses() -> None:
    global CUSTOMER_ADDRESSES
    with open('../data/customers_addresses.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        CUSTOMER_ADDRESSES = [
            CustomerAddress(
                id=int(row[0]),
                city=row[1],
                street=row[2],
                house=int(row[3]),
                entrance=int(row[4]),
                floor=int(row[5]),
                flat=int(row[6]),
                customer_id=int(row[7]),
            ) for row in reader]


def load_rest_addresses() -> None:
    global REST_ADDRESSES
    with open('../data/restaurants_addresses.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        REST_ADDRESSES = [
            RestAddress(
                id=int(row[0]),
                city=row[1],
                street=row[2],
                house=int(row[3]),
                restaurant_id=int(row[4]),
            ) for row in reader]


def generate_cust_address(id_: int) -> CustomerAddress:
    return CustomerAddress(
        id=id_,
        city=random.choice(CITIES),
        street=random.choice(STREETS),
        house=random.randint(1, 999),
        entrance=random.randint(1, 5),
        floor=random.randint(1, 30),
        flat=random.randint(1, 999),
        customer_id=CUSTOMERS[id_ % len(CUSTOMERS)].id
    )


def generate_rest_address(id_: int) -> RestAddress:
    return RestAddress(
        id=id_,
        city=random.choice(CITIES),
        street=random.choice(STREETS),
        house=random.randint(1, 999),
        restaurant_id=RESTAURANTS[id_ % len(RESTAURANTS)].id
    )

def write_address():
    with open('../data/customers_addresses.csv', 'w') as f:
        for idx in range(1, 5001):
            a = generate_cust_address(idx)
            f.write(f'{a.id},{a.city},{a.street},{a.house},{a.entrance},{a.floor},{a.flat},{a.customer_id}\n')

    with open('../data/restaurants_addresses.csv', 'w') as f:
        for idx in range(1, 200001):
            a = generate_rest_address(idx)
            f.write(f'{a.id},{a.city},{a.street},{a.house},{a.restaurant_id}\n')


def gen():
    load_cities()
    load_streets()
    load_customers()
    load_restaurants()
    write_address()


if __name__ == '__main__':
    gen()
