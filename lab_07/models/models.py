import datetime
from dataclasses import dataclass
from typing import Optional

import peewee as pw
from playhouse.postgres_ext import BinaryJSONField

from .base import BaseModel


class Employees(BaseModel):
    id = pw.IntegerField(primary_key=True)
    first_name = pw.CharField()
    last_name = pw.CharField()
    employed_since = pw.DateField()
    birthdate = pw.DateField()
    rating = pw.FloatField()
    salary = pw.IntegerField()
    email = pw.CharField()
    phone_number = pw.CharField()


@dataclass
class EmployeesObj:
    id: int
    first_name: str
    last_name: str
    employed_since: str
    birthdate: str
    rating: Optional[float]
    salary: Optional[float]
    email: str
    phone_number: str

    @staticmethod
    def from_dict(d: dict) -> 'EmployeesObj':
        return EmployeesObj(
            id=int(d['id']),
            first_name=str(d['first_name']),
            last_name=str(d['last_name']),
            employed_since=str(d['employed_since']),
            birthdate=str(d['birthdate']),
            salary=float(d['salary']) if d['salary'] else None,
            rating=float(d['rating']) if d['rating'] else None,
            email=str(d['email']) if d['email'] else None,
            phone_number=str(d['phone_number']) if d['phone_number'] else None,
        )

    @classmethod
    def fields(cls) -> tuple:
        return tuple(cls.__dict__['__annotations__'].keys())


class Customers(BaseModel):
    id = pw.IntegerField(primary_key=True)
    first_name = pw.CharField()
    last_name = pw.CharField()
    birthdate = pw.DateField()
    email = pw.CharField()
    phone_number = pw.CharField()
    registered_at = pw.DateTimeField()


class Restaurants(BaseModel):
    id = pw.IntegerField(primary_key=True)
    name = pw.CharField()
    rating = pw.FloatField()


@dataclass
class RestaurantsObj:
    id: int
    name: str
    rating: float

    @staticmethod
    def from_dict(d: dict) -> 'RestaurantsObj':
        return RestaurantsObj(
            id=int(d['id']),
            name=str(d['name']),
            rating=float(d['rating']),
        )

    @classmethod
    def fields(cls) -> tuple:
        return tuple(cls.__dict__['__annotations__'].keys())


class Products(BaseModel):
    id = pw.IntegerField(primary_key=True)
    name = pw.CharField()
    price = pw.IntegerField()
    restaurant = pw.ForeignKeyField(Restaurants, on_delete='cascade', db_column='restaurant_id')


@dataclass
class ProductsObj:
    id: int
    name: str
    price: float
    restaurant_id: int

    @classmethod
    def fields(cls) -> tuple:
        return tuple(cls.__dict__['__annotations__'].keys())

    @staticmethod
    def from_dict(d: dict) -> 'ProductsObj':
        return ProductsObj(
            id=int(d['id']),
            name=str(d['name']),
            price=float(d['price']),
            restaurant_id=int(d['restaurant_id']),
        )


class Orders(BaseModel):
    id = pw.IntegerField()
    customer_id = pw.ForeignKeyField(Customers, on_delete='cascade')
    dst_address = pw.IntegerField()
    src_address = pw.IntegerField()
    restaurant_id = pw.ForeignKeyField(Restaurants, on_delete='cascade')
    employee = pw.ForeignKeyField(Employees, on_delete='cascade', db_column='employee_id')
    created_at = pw.DateTimeField()
    order_number = pw.IntegerField()
    status = pw.IntegerField()


@dataclass
class OrdersObj:
    id: int
    customer_id: int
    dst_address: int
    src_address: int
    restaurant_id: int
    employee_id: int
    created_at: str
    order_number: int
    status: int

    @classmethod
    def fields(cls) -> tuple:
        return tuple(cls.__dict__['__annotations__'].keys())

    @staticmethod
    def from_dict(d: dict) -> 'OrdersObj':
        return OrdersObj(
            id=int(d['id']),
            dst_address=int(d['dst_address']),
            src_address=int(d['src_address']),
            customer_id=int(d['customer_id']),
            restaurant_id=int(d['restaurant_id']),
            employee_id=int(d['employee_id']),
            created_at=str(d['created_at']),
            order_number=int(d['order_number']),
            status=int(d['status']),
        )


class OrderDetails(BaseModel):
    id = pw.IntegerField()
    product_id = pw.ForeignKeyField(Products, on_delete='cascade')
    amount = pw.IntegerField()


class Employees_JSONB(BaseModel):
    data = BinaryJSONField()
    id = pw.IntegerField()
