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


class Products(BaseModel):
    id = pw.IntegerField(primary_key=True)
    name = pw.CharField()
    price = pw.IntegerField()
    restaurant = pw.ForeignKeyField(Restaurants, on_delete='cascade', db_column='restaurant_id')


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


class OrderDetails(BaseModel):
    id = pw.IntegerField()
    product_id = pw.ForeignKeyField(Products, on_delete='cascade')
    amount = pw.IntegerField()


class Employees_JSONB(BaseModel):
    data = BinaryJSONField()
    id = pw.IntegerField()
