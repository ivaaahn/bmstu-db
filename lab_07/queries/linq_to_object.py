from typing import Optional

from models import (
    ProductsObj,
    RestaurantsObj,
    OrdersObj,
    EmployeesObj, Products, Restaurants, Employees, Orders,
)
from py_linq import Enumerable
from csv import DictReader

import peewee as pw

PREFIX = '/home/ivaaahn/dev/bmstu/bmstu-db/base__(lab_01)/data'


class Models:
    F_PRODUCTS = f'{PREFIX}/products.csv'
    F_RESTAURANTS = f'{PREFIX}/restaurants.csv'
    F_ORDERS = f'{PREFIX}/orders.csv'
    F_EMPLOYEES = f'{PREFIX}/employees.csv'

    def __init__(self):
        self.products: Optional[Enumerable] = None
        self.restaurants: Optional[Enumerable] = None
        self.orders: Optional[Enumerable] = None
        self.employees: Optional[Enumerable] = None

        self.load()

    def _load_products(self):
        with open(self.F_PRODUCTS, newline='') as fd:
            reader = DictReader(fd, fieldnames=ProductsObj.fields(), delimiter=';')
            products = []
            for row in reader:
                products.append(ProductsObj.from_dict(row))
                if int(row['id']) > 250:
                    break

            self.products = Enumerable(products)

    def _load_restaurants(self):
        with open(self.F_RESTAURANTS, newline='') as fd:
            reader = DictReader(fd, fieldnames=RestaurantsObj.fields(), delimiter=';')
            restaurants = []
            for row in reader:
                restaurants.append(RestaurantsObj.from_dict(row))
                if int(row['id']) > 250:
                    break

            self.restaurants = Enumerable(restaurants)

    def _load_orders(self):
        with open(self.F_ORDERS, newline='') as fd:
            reader = DictReader(fd, fieldnames=OrdersObj.fields(), delimiter=',')
            orders = []
            for row in reader:
                orders.append(OrdersObj.from_dict(row))
                if int(row['id']) > 250:
                    break

                self.orders = Enumerable(orders)

    def _load_employees(self):
        with open(self.F_EMPLOYEES, newline='') as fd:
            reader = DictReader(fd, fieldnames=EmployeesObj.fields(), delimiter=',')
            employees = []
            for row in reader:
                employees.append(EmployeesObj.from_dict(row))
                if int(row['id']) > 250:
                    break

            self.employees = Enumerable(employees)

    def load(self):
        self._load_products()
        self._load_restaurants()
        self._load_employees()
        self._load_orders()


#
LINQ_TO_OBJECT_DESCR: dict[int, tuple[str, str]] = {
    1: (
        'Топ 10 самых дорогих блюд, содержащих слово "салат"/"лук"',
        '''
            select
                p.id as product_id,
                p.name as product_name,
                r.name as restaurant,
                p.price as price
            from products p
                   join restaurants r on p.restaurant_id = r.id
            where p.name like '%салат%'
            order by p.price desc
            limit 10;
        '''
    ),
    2: (
        'Продукты, цена которых не больше 100 у.е. (сначала дешевые)',
        '''
        select
            name,
            price
        from products p
        where price <= 100
        order by price;
        '''
    ),
    3: (
        'Доставщики, доставившие >= 100 заказов и число заказов, которое он доставил. (по убыванию кол-ва)',
        '''
        select
            e.id as employee_id,
            e.first_name as employee_name,
            count(o.id) as number_of_orders
        from orders o
            join employees e on o.employee_id = e.id
        group by e.id, e.first_name
        having count(o.id) > 100
        order by count(o.id);
        '''
    ),
    4: (
        'Ресторан и средняя цена продуктов в нем',
        '''
            select
                r.name as name,
                avg(p.price) as avgprice
            from restaurants r
                    join products p on r.id = p.restaurant_id
            group by r.id, r.name;
            '''
    ),
    5: (
        'Топ 10 зарплат работников',
        '''
        select
            id,
            first_name,
            salary
        from employees
        order by salary desc
        limit 10;
        '''
    ),
}


#
#
def linq_to_objects(m: Models):
    return {
        1: [
            ["prod_id", "prod_name", 'rest_name', 'prod_price'],
            [
                [row['prod_id'], row['prod_name'], row['rest_name'], row['prod_price']] for row in
                (
                    m.products.select(
                        lambda r: {'id': r.id, 'name': r.name, 'rest_id': r.restaurant_id, 'price': r.price})
                        .join(
                        m.restaurants,
                        lambda r: r['rest_id'],
                        lambda r: r.id,
                        lambda r: {
                            # 'rest_id': r[0]['id'],
                            'prod_id': r[0]['id'],
                            'prod_name': r[0]['name'],
                            'rest_name': r[1].name,
                            'prod_price': r[0]['price']
                        }
                    )
                        .where(lambda r: 'лук' in str(r['prod_name']).lower())
                        .order_by(lambda r: r['prod_price'])
                        .take(10)
                )
            ]
        ],
        2: [
            ["name", "price"],
            [
                [row['name'], row['price']] for row in
                (
                    m.products.select(lambda r: {'name': r.name, 'price': r.price})
                    .where(lambda r: r['price'] <= 100)
                    .order_by(key=lambda r: r['price'])
                )
            ]
        ],
        3: [
            ["employee_id", 'name', "number_of_orders"],
            [
                [row['employee_id'], row['name'], row['number_of_orders']] for row in
                (
                    m.orders.join(
                        m.employees,
                        lambda r: r.employee_id,
                        lambda r: r.id,
                        lambda r: {'employee_id': r[1].id, 'name': r[1].first_name}
                    )
                    .group_by(
                        key_names=['employee_id', 'name'],
                        key=lambda x: (x['employee_id'], x['name'],))
                    .select(
                        lambda r: {
                            'employee_id': r.key.employee_id,
                            'name': r.key.name,
                            'number_of_orders': r.count()
                        }
                    )
                    .where(
                        lambda r: r['number_of_orders'] > 1
                    )
                    .order_by_descending(key=lambda r: r['number_of_orders'])
                )
            ]
        ],
        4: [
            ["name", "avg_price"],
            [
                [row['name'], round(row['avg_price'], 3)] for row in
                (
                    m.products.join(
                        m.restaurants,
                        outer_key=lambda r: r.restaurant_id,
                        inner_key=lambda r: r.id,
                        result_func=lambda r: {'name': r[1].name, 'price': r[0].price}
                    )
                    .group_by(
                        key_names=['name'],
                        key=lambda x: x['name'],
                        result_func=lambda x: x,
                    )
                    .select(
                        lambda r: {
                            'name': r.key.name,
                            'avg_price': r.avg(lambda x: x['price'])
                        }
                    )
                )
            ]
        ],
        5: [
            ['id', 'name', 'salary'],
            [
                [row['employee_id'], row['name'], row['salary']] for row in
                (
                    m.employees.select(
                        lambda r: {
                            'employee_id': r.id,
                            'name': r.first_name,
                            'salary': r.salary,
                        }
                    )
                    .order_by_descending(lambda x: x['salary'])
                    .take(10)
                )
            ]
        ],
    }


LINQ_TO_OBJECT_QUERIES = {
    1: [
        ["prod_id", "prod_name", 'rest_name', 'prod_price'],
        [
            [row.prod_id, row.prod_name, row.restaurant.rest_name, row.prod_price] for row in
            (
                (Products.select(
                    Products.id.alias('prod_id'),
                    Products.name.alias('prod_name'),
                    Restaurants.name.alias('rest_name'),
                    Products.price.alias('prod_price'),
                ).join(Restaurants)
                 .where(Products.name.like('%салат%'))
                 .order_by(-Products.price).limit(10))
            )
        ]
    ],
    2: [
        ["name", "price"],
        [
            [row.name, row.price] for row in
            (
                Products.select(
                    Products.name,
                    Products.price,
                ).where(Products.price <= 100)
                    .order_by(Products.price))
        ]
    ],
    3: [
        ["employee_id", 'name', "number_of_orders"],
        [
            [row.employee.id, row.employee.name, row.number_of_orders] for row in
            (Orders.select(
                Employees.id,
                Employees.first_name.alias('name'),
                pw.fn.COUNT(Orders.id).alias("number_of_orders"))
             .join(Employees)
             .group_by(Employees.id, Employees.first_name)
             .having(pw.fn.COUNT(Orders.id) >= 100)
             .order_by(-pw.fn.COUNT(Orders.id))
             )
        ]
    ],
    4: [
        ["name", "avg_price"],
        [
            [row.name, row.avgprice] for row in
            (Restaurants.select(
                Restaurants.name,
                pw.fn.AVG(Products.price).alias("avgprice"),
            ).join(Products)
             .group_by(Restaurants.id))
        ]
    ],
    5: [
        ['id', 'name', 'salary'],
        [
            [row.employee_id, row.name, row.salary] for row in
            (Employees.select(
                Employees.id.alias('employee_id'),
                Employees.first_name.alias('name'),
                Employees.salary.alias('salary'),
            ).order_by(-Employees.salary)
             .limit(10))
        ]
    ],
}
