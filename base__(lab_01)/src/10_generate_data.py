import csv
import random
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from random import choice, randint
from datetime import timedelta

FILE_TO_SAVE_ORDERS = './data/orders.csv'
FILE_TO_SAVE_ORDER_DETAILS = './data/order_details.csv'


@dataclass
class Order:
    id: int
    customer_id: int  # 1-1000
    dst_address: int  # 1-1000
    src_address: int  # 1-1000
    restaurant_id: int  # 1-1000
    employee_id: int
    created_at: str
    order_number: int
    status: int


@dataclass
class Product:
    id: int
    name: str
    price: float
    restaurant_id: int


@dataclass
class Customer:
    id: int
    first_name: str
    last_name: Optional[str]
    birthdate: Optional[date]
    email: Optional[str]
    phone_number: str
    registered_at: datetime


@dataclass
class Employee:
    id: int
    first_name: str
    last_name: str
    employed_since: date
    birthdate: date
    rating: float
    salary: float
    email: str
    phone_number: str


@dataclass
class Restaurant:
    id: int
    name: str
    rating: float


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


@dataclass
class OrderStatus:
    id: int
    name: str


@dataclass
class OrderDetails:
    order_id: int
    product_id: int
    amount: int


CUSTOMER_ADDRESSES: list[CustomerAddress] = []
REST_ADDRESSES: list[RestAddress] = []
CUSTOMERS: list[Customer] = []
EMPLOYEES: list[Employee] = []
RESTAURANTS: list[Restaurant] = []
ORDER_STATUSES: list[OrderStatus] = []
PRODUCTS: list[Product] = []

ORDERS: list[Order] = []
DETAILS: list[OrderDetails] = []


def load_customer_addresses() -> None:
    global CUSTOMER_ADDRESSES
    with open('./data/customers_addresses.csv', newline='') as f:
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
    with open('./data/restaurants_addresses.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        REST_ADDRESSES = [
            RestAddress(
                id=int(row[0]),
                city=row[1],
                street=row[2],
                house=int(row[3]),
                restaurant_id=int(row[4]),
            ) for row in reader]


def load_customers() -> None:
    global CUSTOMERS
    with open('./data/customers.csv', newline='') as f:
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


def load_employees() -> None:
    global EMPLOYEES
    with open('./data/employees.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        EMPLOYEES = [
            Employee(
                id=int(row[0]),
                first_name=row[1],
                last_name=row[2],
                employed_since=datetime.strptime(row[3], "%Y-%m-%d"),
                birthdate=datetime.strptime(row[4], "%Y-%m-%d"),
                rating=float(row[5]),
                salary=float(row[6]),
                email=row[7],
                phone_number=row[8],
            ) for row in reader]


def load_restaurants() -> None:
    global RESTAURANTS
    with open('./data/restaurants.csv', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        RESTAURANTS = [
            Restaurant(
                id=int(row[0]),
                name=row[1],
                rating=float(row[2]),
            ) for row in reader]


def load_order_statuses() -> None:
    global ORDER_STATUSES
    with open('./data/order_statuses.csv', newline='') as f:
        reader = csv.reader(f, delimiter=',')
        ORDER_STATUSES = [
            OrderStatus(
                id=int(row[0]),
                name=row[1],
            ) for row in reader]


def load_products() -> None:
    global PRODUCTS
    with open('./data/products2.csv', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        PRODUCTS = [
            Product(
                id=int(row[0]),
                name=row[1],
                price=float(row[2]),
                restaurant_id=int(row[3])
            ) for row in reader]


def _random_date(start_datetime, end_datetime):
    time_between_dates = end_datetime - start_datetime
    days_between_dates = time_between_dates.days
    days = random.randrange(days_between_dates)
    h = randint(0, 23)
    m = randint(0, 59)
    s = randint(0, 59)

    random_date = start_datetime + timedelta(days=days, hours=h, minutes=m, seconds=s)
    return random_date


def gen_order() -> None:
    created_at = _random_date(datetime(2021, 1, 1, 0, 0), datetime(2021, 10, 1, 0, 0))
    order_id = len(ORDERS) + 1

    customer = choice(CUSTOMERS)
    cust_addr = choice([a for a in CUSTOMER_ADDRESSES if a.customer_id == customer.id])

    city = cust_addr.city
    restaurant_address = choice([a for a in REST_ADDRESSES if a.city == city])
    restaurant_id = restaurant_address.restaurant_id

    order = Order(
        id=order_id,
        customer_id=customer.id,
        dst_address=cust_addr.id,
        src_address=restaurant_address.id,
        restaurant_id=restaurant_id,
        employee_id=choice(EMPLOYEES).id,
        created_at=created_at,
        order_number=random.randint(1, 99999),
        status=5,
    )

    ORDERS.append(order)
    gen_order_details(order_id, restaurant_id)


def gen_order_details(order_id: int, rest_id: int):
    available_products = [prod for prod in PRODUCTS if prod.restaurant_id == rest_id]
    products = random.sample(available_products, min(randint(1, 6), len(available_products)))
    DETAILS.extend([OrderDetails(order_id=order_id, product_id=p.id, amount=randint(1, 3)) for p in products])


def load_data():
    load_rest_addresses()
    load_customer_addresses()
    load_customers()
    load_employees()
    load_restaurants()
    load_order_statuses()
    load_products()


def write_orders():
    with open(FILE_TO_SAVE_ORDERS, "w") as f:
        for order in ORDERS:
            string = f'{order.id},{order.customer_id},{order.dst_address},{order.src_address},{order.restaurant_id},' \
                     f'{order.employee_id},{order.created_at},{order.order_number},{order.status}\n'
            f.write(string)


def write_order_details():
    with open(FILE_TO_SAVE_ORDER_DETAILS, "w") as f:
        for detail in DETAILS:
            string = f'{detail.order_id},{detail.product_id},{detail.amount}\n'
            f.write(string)


def gen_orders():
    for idx in range(100000):
        gen_order()
        if not idx % 1000:
            print(idx, ': done;')


if __name__ == '__main__':
    load_data()
    gen_orders()
    write_orders()
    write_order_details()
