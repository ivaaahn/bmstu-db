-- 1) Подсчитывает размер премии для сотрудника.
create function get_employee_award(IN rating float8, IN num_of_orders bigint, IN curr_salary float8) RETURNS FLOAT8 as
$$
BEGIN
    return rating * num_of_orders / 30 * curr_salary / 10;
END;
$$ language plpgsql;


-- select get_number_of_orders_from_city('Москва')

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


-- 2

-- МОЖНО ТАК

-- DROP TABLE IF EXISTS typedtbl;
-- CREATE TABLE typedtbl (
--     order_id int,
--     customer text,
--     employee varchar,
--     price double precision,
--     units_of_products bigint
-- );
--
-- create or replace function ext_orders_info() returns setof typedtbl as
-- $$
-- BEGIN
--     RETURN QUERY select o.id                                   as order_id,
--                         concat(c.first_name, ' ', c.last_name) as customer,
--                         e.first_name                           as employee,
--                         sum(p.price * od.amount)               as price,
--                         count(od.amount)                       as units_of_products
--                  from orders o
--                           join order_details od on o.id = od.order_id
--                           join products p on od.product_id = p.id
--                           join customers c on o.customer_id = c.id
--                           join employees e on o.employee_id = e.id
--                  group by o.id, c.first_name, c.last_name, e.first_name
--                  order by price desc;
-- end;
-- $$ language plpgsql;

-- select * from ext_orders_info(NULL::typedtbl)

-- ИЛИ ТАК

create or replace function ext_orders_info()
    returns table
            (
                order_id          int,
                customer          text,
                employee          varchar,
                price             double precision,
                units_of_products bigint
            )
as
$$
select o.id                                   as order_id,
       concat(c.first_name, ' ', c.last_name) as customer,
       e.first_name                           as employee,
       sum(p.price * od.amount)               as price,
       count(od.amount)                       as units_of_products
from orders o
         join order_details od on o.id = od.order_id
         join products p on od.product_id = p.id
         join customers c on o.customer_id = c.id
         join employees e on o.employee_id = e.id
group by o.id, c.first_name, c.last_name, e.first_name
$$ language SQL;

SELECT *
FROM ext_orders_info();

-- 3

create function get_top_X_price(in x int, in prod_name varchar)
    returns table
            (
                product_id   int,
                product_name varchar,
                restaurant   text,
                price        float8
            )
as
$$
BEGIN
    create temp table tbl
    (
        product_id   int,
        product_name varchar,
        restaurant   text,
        price        float8
    );

    insert into tbl(product_id, product_name, restaurant, price)
    select p.id as product_id, p.name as product_name, r.name as restaurant, p.price as price
    from products p
             join restaurants r on p.restaurant_id = r.id
    where p.name like concat('%', prod_name, '%');

    return query
        select *
        from tbl
        order by price desc
        limit x;

end;
$$ language plpgsql;

select *
from get_top_X_price(11, 'салат');


-- 4

CREATE OR REPLACE FUNCTION get_post_comments(parent_comment_id int)
    RETURNS TABLE
            (
                id        int,
                title     varchar,
                parent_id int,
                level     int
            )
AS
$$
BEGIN
    RETURN QUERY with recursive rec as (
        select c.id, c.title, c.parent_id, 0 as level
        from comments c
        where c.parent_id = parent_comment_id

        union all

        select c.id, c.title, c.parent_id, rec.level + 1 as level
        from rec
                 join comments c on rec.id = c.parent_id
    )
                 select *
                 from rec;
END;
$$ LANGUAGE PLPGSQL;

select *
from get_post_comments(0);

-- 5
CREATE PROCEDURE change_employee_salary(in employee int, in delta float8) AS
$$
BEGIN
    UPDATE employees
    SET salary = salary + delta
    WHERE id = employee;
END;
$$ LANGUAGE PLPGSQL;

select *
from employees
where id = 1;

call change_employee_salary(1, 300);

-- 6
CREATE PROCEDURE find_root_comment(from_id int)
AS
$$
DECLARE
    parent_id int;
    curr_id   int;
BEGIN
    RAISE NOTICE 'You are now at %.', from_id;
    SELECT c.parent_id
    FROM comments c
    WHERE c.id = from_id
    INTO parent_id;
    IF parent_id = 0 THEN
        RAISE NOTICE 'It is root comment!';
    ELSE
        SELECT c.parent_id
        FROM comments c
        WHERE c.id = from_id
        INTO curr_id;
        RAISE NOTICE 'Keep going!';
        CALL find_root_comment(curr_id);
    END IF;
END;
$$ LANGUAGE PLPGSQL;
CALL find_root_comment(15);


-- 7
CREATE PROCEDURE fetch_restaurants_by_rating(IN min_rating float8)
AS
$$
DECLARE
    cur CURSOR FOR
        SELECT *
        FROM restaurants r
        where r.rating >= min_rating
        order by r.rating desc;
BEGIN
    for rest in cur
        loop
            raise notice 'Ресторан % с рейтингом %', rest.name, rest.rating;
        end loop;
END;
$$ LANGUAGE PLPGSQL;

CALL fetch_restaurants_by_rating(4.0);

-- 8
CREATE PROCEDURE get_db_metadata(dbname VARCHAR)
AS
$$
DECLARE
    dbid        INT;
    dbconnlimit INT;
    dbenc       varchar;
BEGIN
    SELECT pg.oid, pg.datconnlimit, pg_encoding_to_char(pg.encoding)
    FROM pg_database pg
    WHERE pg.datname = dbname
    INTO dbid, dbconnlimit, dbenc;
    RAISE NOTICE 'DB: %, ENCODING: %, ID: %, CONNECTION LIMIT: %', dbname, dbenc, dbid, dbconnlimit;
END;
$$ LANGUAGE PLPGSQL;
CALL get_db_metadata('labs_db');


-- 9
CREATE FUNCTION get_employee_rating()
    RETURNS TRIGGER
AS
$$
declare
    rating float8;
BEGIN
    select e.rating
    from employees e
    where e.id = new.employee_id
    into rating;

    IF rating >= 4 THEN
        RAISE NOTICE 'Ваш заказ доставляет один из лучших курьеров! Его рейтинг - %', rating;
    ELSE
        RAISE NOTICE 'Упс, будьте осторожны с курьером... Его рейтинг - %', rating;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER employee_info
    AFTER INSERT
    ON orders
    FOR ROW
EXECUTE PROCEDURE get_employee_rating();

insert into orders(customer_id, dst_address, src_address, restaurant_id, employee_id, order_number, status)
values (1, 2, 3, 4, 1, 777, 1);


-- 10
create table if not exists waiting_products
(
    product_id int,
    name       varchar,
    price      float8,
    restaurant varchar
);


CREATE OR REPLACE FUNCTION insert_product()
    RETURNS TRIGGER
AS
$$
BEGIN
    IF NOT EXISTS(
            SELECT product
            FROM Top50ExpensiveProducts top
            WHERE top.product = NEW.product
              and top.price = NEW.price
              and top.restaurant = NEW.restaurant
        )
    THEN
        IF NOT EXISTS(
                SELECT product_id
                FROM waiting_products wp
                WHERE wp.product_id = NEW.pid
            )
        THEN
            INSERT INTO waiting_products
            VALUES (NEW.pid, NEW.product, NEW.price, NEW.restaurant);
            RAISE NOTICE 'We will consider your application!';
            RETURN NEW;
        END IF;
        RAISE NOTICE 'Your product already waiting its turn to process...';
    ELSE
        RAISE NOTICE 'This product already exists in top!';
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE PLPGSQL;

create view Top50ExpensiveProducts as
select p.id as pid, p.name as product, p.price as price, r.name as restaurant
from products p
         join restaurants r on p.restaurant_id = r.id
order by p.price desc
limit 50;


CREATE TRIGGER insert_product_in_top
    INSTEAD OF INSERT
    ON Top50ExpensiveProducts
    FOR ROW
EXECUTE PROCEDURE insert_product();

select *
from Top50ExpensiveProducts;

insert into Top50ExpensiveProducts
values (99999999, 'Тест продукт', 99999, 'KFC');


insert into Top50ExpensiveProducts
values (17938, 'Чашушули на кеци', 90450, 'Хинкальный Дом')