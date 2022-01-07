from models import *
LINQ_TO_OBJECT_DESCR = {
    1: (
        'Топ 10 самых дорогих блюд, содержащих слово "салат"',
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

LINQ_TO_OBJECT_QUERIES = {
    1: [
        ["prod_id", "prod_name", 'rest_name', 'prod_price'],
        [
            [row.prod_id, row.prod_name, row.restaurant.rest_name, row.prod_price] for row in
            (Products.select(
                Products.id.alias('prod_id'),
                Products.name.alias('prod_name'),
                Restaurants.name.alias('rest_name'),
                Products.price.alias('prod_price'),
            ).join(Restaurants)
             .where(Products.name.like('%салат%'))
             .order_by(-Products.price).limit(10))
        ]
    ],
    2: [
        ["name", "price"],
        [
            [row.name, row.price] for row in
            (Products.select(
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