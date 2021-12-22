import asyncio
import os
from pprint import pprint

from asyncpg import Connection

from config import setup_config
from db import setup_connection

PATH = '/home/ivaaahn/dev/bmstu/bmstu-db/lab_06'


async def task1(conn: Connection, **kwargs):
    res = await conn.fetch('select email from customers where id=2')
    print(*res)


# Получить 10 последних заказов по Москве
async def task2(conn: Connection, **kwargs):
    query = '''
    select o.id                                   as order_id,
       o.created_at,
       concat(c.first_name, ' ', c.last_name) as customer,
       r.name                                 as restaurant,
       concat(e.first_name, ' ', e.last_name) as employee
from orders o
         join customers c on c.id = o.customer_id
         join restaurants r on o.restaurant_id = r.id
         join employees e on o.employee_id = e.id
where o.dst_address in (select ca.customer_id from customers_addresses ca where ca.city = 'Москва')
order by created_at desc
limit 10;
'''

    res = await conn.fetch(query)
    pprint(res)


#  рестораны, чьи продажи товаров хуже среднего + номер по порядку
async def task3(conn: Connection, **kwargs):
    query = '''
    with avg_t as (select avg(ext.summary_amounts) as average_qty
               from (select sum(od.amount) as summary_amounts
                     from restaurants r
                              join products p on r.id = p.restaurant_id
                              join order_details od on p.id = od.product_id
                     group by r.name) as ext),
     sum_t as (select r.name as restaurant, sum(od.amount) as summary_qty
               from restaurants r
                        join products p on r.id = p.restaurant_id
                        join order_details od on p.id = od.product_id
               group by r.name
               order by summary_qty)
select sum_t.*, row_number() over (order by restaurant)
from sum_t,
     avg_t
where sum_t.summary_qty < avg_t.average_qty
order by summary_qty desc;
'''

    res = await conn.fetch(query)
    pprint(res)


async def task4(conn: Connection, **kwargs):
    query = '''
     SELECT pg.oid, pg.datconnlimit, pg_encoding_to_char(pg.encoding)
    FROM pg_database pg
    WHERE pg.datname = 'labs_db'
    '''

    res = await conn.fetch(query)
    pprint(res)


async def task5(conn: Connection, **kwargs):
    query = '''
        select id as emp_id, get_employee_award(rating, num_of_orders, curr_salary) as res
from (
         select e.id,
                e.rating,
                e.salary   as curr_salary,
                count(o.*) as num_of_orders
         from employees e
                  join orders o on e.id = o.employee_id
--          where e.id = 2
             and extract(MONTH from o.created_at) = extract(month from now()) - 1
         group by e.id
     ) as eo
order by res desc;
    '''

    res = await conn.fetch(query)
    pprint(res)


async def task6(conn: Connection, **kwargs):
    query = '''
    select *
from get_top_X_price(11, 'салат');
'''

    res = await conn.fetch(query)
    pprint(res)


async def task7(conn: Connection, **kwargs):
    query = '''
    call change_employee_salary(1, 300);
'''

    res = await conn.execute(query)


async def task8(conn: Connection, **kwargs):
    query = '''
    select current_database()	
    '''

    res = await conn.fetch(query)
    pprint(res)


async def task9(conn: Connection, **kwargs):
    query = '''
    drop table if exists chefs;
    create table chefs(
        id serial primary key,
        name varchar not null,
        rating float NOT NULL check ( rating >= 0.0 AND rating <= 5.0 )        
    );
    '''

    res = await conn.execute(query)
    pprint(res)


async def task10(conn: Connection, **kwargs):
    name_ = input("Input chef's name: ")
    try:
        rating_ = float(input("Input chef's rating: "))
    except:
        print("Incorrect rating!")
    else:
        return

    query = f"""
    insert into chefs(name, rating) values
    ('{name_}', '{rating_}');
    """

    res = await conn.execute(query)
    pprint(res)


async def task11(conn: Connection, **kwargs):
    filename = input("Input filename: ")
    path = f'{PATH}/{filename}.json'

    query_create = f"drop table if exists received_orders;create table received_orders ( data jsonb );COPY received_orders from '{path}'"
    await conn.execute(query_create)

    select = '''select distinct r.name from restaurants r where r.id in (
                    select (data->'restaurant_id')::int as rest_id from received_orders
                );'''

    pprint(await conn.fetch(select))


async def main():
    conn = await setup_connection(setup_config(os.environ.get("CONFIG_L6")))

    tasks = {
        1: task1,
        2: task2,
        3: task3,
        4: task4,
        5: task5,
        6: task6,
        7: task7,
        8: task8,
        9: task9,
        10: task10,
        11: task11,
    }

    print("Your choice???\n")

    print(
        '''
        1. Выполнить скалярный запрос;
        2. Выполнить запрос с несколькими соединениями (JOIN);
        3. Выполнить запрос с ОТВ(CTE) и оконными функциями;
        4. Выполнить запрос к метаданным;
        5. Вызвать скалярную функцию (написанную в ЛР3);
        6. Вызвать многооператорную или табличную функцию (написанную в ЛР3);
        7. Вызвать хранимую процедуру (написанную в третьей лабораторной работе);
        8. Вызвать системную функцию или процедуру;
        9. Создать таблицу в базе данных, соответствующую тематике БД;
        10. Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY.
        11. Поиск ресторанов по заказам JSON
        '''
    )

    flag = True

    while flag:

        try:
            choice = int(input())
        except:
            print("Incorrect choice")
            flag = False
        else:
            await tasks[choice](conn)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
