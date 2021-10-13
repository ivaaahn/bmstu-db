-- 1. Инструкция SELECT, использующая предикат сравнения.
-- Получить все заказ Зой Герасимовых
select o.id                                   as order_id,
       date(o.created_at)                     as order_date,
       concat(c.first_name, ' ', c.last_name) as customer,
       p.name                                 as product_name,
       od.amount                              as qty,
       r.name                                 as restaurant
from orders o
         join customers c on o.customer_id = c.id
         join order_details od on o.id = od.order_id
         join products p on od.product_id = p.id
         join restaurants r on o.restaurant_id = r.id
where concat(c.first_name, ' ', c.last_name) = 'Зоя Герасимова'
order by o.created_at
limit 10;

-- 2. Инструкция SELECT, использующая предикат BETWEEN.
-- Получить всех клиентов, заказывавших что-то первого сентября
select distinct concat(c.first_name, ' ', c.last_name) as customer,
                date(o.created_at)                     as order_date
from orders o
         join customers c on o.customer_id = c.id
where created_at between '2020-09-01' and '2020-09-02'
order by order_date;

-- 3. Инструкция SELECT, использующая предикат LIKE.
-- Топ10 самых дорогих салатов
select p.id as product_id, p.name as product_name, r.name as restaurant, p.price as price
from products p
         join restaurants r on p.restaurant_id = r.id
where p.name like '%салат%'
order by p.price desc
limit 10;


-- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом.
-- Получить 10 последних заказов по Москве
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

-- 5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом.
-- Получить все рестораны, в меню которых имеются салаты
select *
from restaurants r
where exists(select 1 from products p where p.name like '%салат%' and p.restaurant_id = r.id);

-- 6. Инструкция SELECT, использующая предикат сравнения с квантором.
-- Количество работников, которые могут позволить себе любой заказ, сделанный 4-ым покупателем
select count(*)
from employees e
where e.salary > all (select sum((p.price * od.amount)) as full_price
                      from orders o
                               join order_details od on o.id = od.order_id
                               join customers c on o.customer_id = c.id
                               join products p on od.product_id = p.id
                      where o.customer_id = 4
                      group by o.id, c.first_name);

-- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов.
--  Топ 50 клиентов по средней цене заказа
select c.id, concat(c.first_name, ' ', c.last_name) as name, avg(p.price * od.amount) as average_price
from customers c
         left join orders o on c.id = o.customer_id
         join order_details od on o.id = od.order_id
         join products p on od.product_id = p.id
group by c.id
order by average_price desc
limit 50;

-- 8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов
-- Топ 15 дешевых ресторанов по средней цене продуктов
select r.id,
       r.name,
       (select max(p.price) from products p where p.restaurant_id = r.id) as max_price,
       (select avg(p.price) from products p where p.restaurant_id = r.id) as avg_price
from restaurants r
order by avg_price
limit 15;

-- 9. Инструкция SELECT, использующая простое выражение CASE.
--  Получить все заказы с пометкой года
select o.id                                   as order_id,
       concat(c.first_name, ' ', c.last_name) as customer_name,
       (case date_part('year', o.created_at)
            when date_part('year', CURRENT_DATE) then 'this year'
            when date_part('year', CURRENT_DATE) - 1 then 'last year'
            else concat(cast((date_part('year', CURRENT_DATE) - date_part('year', o.created_at)) as varchar(4)),
                        ' years ago')
           end)                               as "when"
from orders o
         join customers c on o.customer_id = c.id
order by customer_name;

-- 10. Инструкция SELECT, использующая поисковое выражение CASE.
select r.id,
       r.name,
       case
           when count(o.*) < 60 then 'Не популярный'
           when count(o.*) < 85 then 'Обычный'
           when count(o.*) < 110 then 'Популярный'
           else 'Очень популярный'
           end as popularity
from restaurants r
         join orders o
              on r.id = o.restaurant_id
group by r.id, r.name
order by r.name;


-- 11. Создание новой временной локальной таблицы из результирующего набора данных инструкции SELECT.
select o.id                                   as order_id,
       concat(c.first_name, ' ', c.last_name) as customer,
       e.first_name                           as employee,
       sum(p.price * od.amount)               as price,
       count(od.amount)                       as untits_of_products
into temporary OrdersExt
from orders o
         join order_details od on o.id = od.order_id
         join products p on od.product_id = p.id
         join customers c on o.customer_id = c.id
         join employees e on o.employee_id = e.id
group by o.id, c.first_name, c.last_name, e.first_name
order by price desc;

select *
from OrdersExt;


-- 12. Инструкция SELECT, использующая вложенные коррелированные подзапросы в
-- качестве производных таблиц в предложении FROM


select *
from products p
         join (select product_id, sum(amount) as summary_qty
               from order_details od
               group by product_id
               order by summary_qty
               limit 1) as od on od.product_id = p.id;


-- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3.
--  Найти самый продаваемый продукт
select *
from products p
where p.id = (select product_id
              from order_details
              group by product_id
              having sum(amount) = (select max(summary_qty)
                                    from (select sum(amount) as summary_qty
                                          from order_details
                                          group by product_id) as od));

-- или так

select *
from products p
         join (select product_id, sum(amount) as summary_qty
               from order_details
               group by product_id
               having sum(amount) = (select max(summary_qty)
                                     from (select sum(amount) as summary_qty
                                           from order_details
                                           group by product_id) as od)) as od on od.product_id = p.id;



-- 14. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY, но без предложения HAVING.
-- самые продаваемые товары (по колву)
select p.id as product_id, p.name as product_name, sum(od.amount) as summary_qty
from products p
         join order_details od on p.id = od.product_id
group by p.id, p.name
order by summary_qty desc
limit 3;

-- 15. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY и предложения HAVING.
-- рестораны, которые продали менее 200 товаров
select r.name as restaurant, sum(od.amount) as summary_qty
from restaurants r
         join products p on r.id = p.restaurant_id
         join order_details od on p.id = od.product_id
group by r.name
having sum(od.amount) < 200
order by summary_qty;


-- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной строки значений.

-- insert into restaurants(name, rating)
-- values ('TestRest', 4.5);

insert into products(id, name, price, restaurant_id)
values (default, 'test_prod', 777, 1);


-- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу результирующего набора данных вложенного подзапроса

-- insert into orders(customer_id, dst_address, src_address, restaurant_id, employee_id, order_number, status)
-- values (1, 5000, 100548, 1, 1, 777, 1);

insert into order_details(order_id, product_id, amount)
select(select max(o.id)
       from orders o
       where o.customer_id = 1
         and o.restaurant_id = 1),
      p.id,
      2
from products p
where p.name = 'Баскет Фри';

-- select *
-- from orders o
--          join order_details od on o.id = od.order_id
--          join products p on od.product_id = p.id
-- where o.customer_id = 1
-- order by o.id desc;


-- 18. Простая инструкция UPDATE.
update products p
set price = p.price * 1.1
where p.id = 1;

-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET.

update products p
set price = (select ceil(avg(price))
             from products
             where restaurant_id = p.restaurant_id
               and id != 1)
where p.id = 1;

-- 20. Простая инструкция DELETE.
--
-- insert into products(id, name, price, restaurant_id)
-- values (default, 'test_prod', 777, 1);

delete
from products
where name = 'test_prod';


-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в предложении WHERE.

delete
from products p
where id = (select od.product_id
            from order_details od
                     join orders o on od.order_id = o.id
            where o.restaurant_id = p.restaurant_id
            group by od.product_id
            order by sum(amount)
            limit 1);

-- 22. Инструкция SELECT, использующая простое обобщенное табличное выражение
-- рестораны, чьи продажи товаров хуже среднего
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
select sum_t.*
from sum_t,
     avg_t
where sum_t.summary_qty < avg_t.average_qty
order by summary_qty desc;


-- 23. Инструкция SELECT, использующая рекурсивное обобщенное табличное выражение.

---------PREPARE-----------
create table comments
(
    id        serial primary key,
    title     varchar,
    parent_id int
);

COPY comments FROM '/home/ivaaahn/dev/bmstu/bmstu-db/base__(lab_01)/data/comments.csv' DELIMITER ',' CSV;
---------PREPARE-----------

with recursive rec as (
    select id, title, parent_id, 0 as level
    from comments c
    where parent_id = 2

    union all

    select c.id, c.title, c.parent_id, rec.level + 1 as level
    from rec
             join comments c on rec.id = c.parent_id
)
select *
from rec;

-- 24. Оконные функции. Использование конструкций MIN/MAX/AVG OVER()

with ext_orders_info as (select c.id                                   as customer_id,
                                concat(c.first_name, ' ', c.last_name) as customer_name,
                                o.id                                   as order_id,
                                sum(od.amount * p.price)               as summary_price
                         from customers c
                                  join orders o on c.id = o.customer_id
                                  join order_details od on o.id = od.order_id
                                  join products p on od.product_id = p.id
                         where c.id = 1
                         group by o.id, c.id, concat(c.first_name, ' ', c.last_name)
                         order by order_id)
select eoi.*,
       sum(summary_price) over (order by order_id)       as summary_expenses,
       ceil(avg(summary_price) over (order by order_id)) as average_expenses
from ext_orders_info eoi;


-- 25. Оконные фнкции для устранения дублей


select *, row_number() over () as id
into temporary names
from (select concat(first_name, ' ', last_name) as fullname
      from customers

      union all

      select concat(first_name, ' ', last_name) as fullname
      from employees

      order by fullname) as tmp;



-- select *
-- from (select id,
--              fullname,
--              row_number() over (partition by fullname order by fullname) as occur
--       from names) as ext_names
-- where occur > 1;


delete
from names
    using (select id,
                  fullname,
                  row_number() over (partition by fullname order by fullname) as occur
           from names) as ext_names
where names.id = ext_names.id
  and occur > 1
returning *;


-- select count(*)
-- from names;


-- ЗАЩИТА ЛАБЫ (Рестораны, на которые клиент потратил больше, чем тратит в среднем на ресторан)
with expenses as (select r.id                  as rest_id,
                         r.name                as rest_name,
                         r.rating              as rest_rating,
                         sum(amount * p.price) as summary_expenses
                  from orders o
                           join customers c on o.customer_id = c.id
                           join order_details od on o.id = od.order_id
                           join products p on od.product_id = p.id
                           join restaurants r on o.restaurant_id = r.id
                  where concat(c.first_name, ' ', c.last_name) = 'Фирс Никонов'
                  group by r.id, r.name
                  order by summary_expenses desc)
select *
from expenses
where summary_expenses > (select avg(summary_expenses) from expenses)
order by summary_expenses;
-- select avg(summary_expenses) from expenses
