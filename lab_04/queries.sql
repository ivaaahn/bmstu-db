CREATE EXTENSION IF NOT EXISTS plpython3u;
-- 1

create or replace function get_employee_award_py(IN rating float8, IN num_of_orders bigint, IN curr_salary float8)
    returns float as
$$
   return round(rating * num_of_orders / 30 * curr_salary / 10)
$$ language plpython3u;

select id as emp_id, get_employee_award_py(rating, num_of_orders, curr_salary) as res
from (
         select e.id,
                e.rating,
                e.salary   as curr_salary,
                count(o.*) as num_of_orders
         from employees e
                  join orders o on e.id = o.employee_id
         where extract(MONTH from o.created_at) = extract(month from now()) - 1
         group by e.id
     ) as eo
order by res desc;


-- 2

create or replace function get_avg_employees_awards_py()
    returns decimal as
$$
    query = """ select id as emp_id, get_employee_award_py(rating, num_of_orders, curr_salary) as res
from (
         select e.id,
                e.rating,
                e.salary   as curr_salary,
                count(o.*) as num_of_orders
         from employees e
                  join orders o on e.id = o.employee_id
         where extract(MONTH from o.created_at) = extract(month from now()) - 1
         group by e.id
     ) as eo
order by res desc; """

    result = plpy.execute(query)
    summary = 0
    for row in result:
        summary += row["res"]

    return summary / len(result)

$$ language plpython3u;

select get_avg_employees_awards_py();

-- 3

create or replace function get_top_x_price_products_py(in x int, in prod_name varchar)
    returns table
            (
                product_id   int,
                product_name varchar,
                restaurant   text,
                price        float8
            )
as
$$
   query = f"""select p.id as product_id, p.name as product_name, r.name as restaurant, p.price as price
   from products p
            join restaurants r on p.restaurant_id = r.id
   where p.name like concat(''%'', prod_name, ''%'');"""

   result = plpy.execute(query)

   for row in result:
       yield ( row["product_id"], row["product_name"], row["restaurant"], row["price"] )

$$ language plpython3u;

select *
from get_top_X_price(11, 'салат');


-- 4

create procedure change_employee_salary_py(in employee int, in delta float8) AS
$$
    plan = plpy.prepare(
        "UPDATE employees SET salary = salary + $1 WHERE id = $2",
        ["float8", "int"]
    )
    plpy.execute(plan, [delta, employee])
$$ LANGUAGE plpython3u;

call change_employee_salary_py(1, 300);

-- 5

create or replace function get_employee_rating_py()
    returns trigger as
$$
    res = plpy.execute(f"select e.rating as rating from employees e where e.id = {TD['new']['employee_id']};")
    if (rating := res[0]["rating"]) >= 4:
        plpy.notice(f"[PY] Ваш заказ доставляет один из лучших курьеров! Его рейтинг - {rating}")
    else:
        plpy.notice(f"[PY] Упс, будьте осторожны с курьером... Его рейтинг - {rating}")
$$ language plpython3u;

CREATE TRIGGER employee_info_py
    AFTER INSERT
    ON orders
    FOR ROW
EXECUTE PROCEDURE get_employee_rating_py();

insert into orders(customer_id, dst_address, src_address, restaurant_id, employee_id, order_number, status)
values (1, 2, 3, 4, 1, 777, 1);

-- 6

create type rest_rating as
(
    rest_id int,
    rating  float8
);

create or replace function set_rest_rating_py(rid int, rating float8)
    returns setof rest_rating
as
$$
    return [(rid, rating)]
$$ language plpython3u;

select * from set_rest_rating_py(1, 4.2);

