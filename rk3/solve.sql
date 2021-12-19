-- Студент: Ивахненко Дмитрий (ИУ7-56Б)
-- Вариант: ЧЕТЫРЕ

DROP DATABASE IF EXISTS mct3;
CREATE DATABASE mct3;

CREATE TABLE employees
(
    id         SERIAL PRIMARY KEY,
    full_name  VARCHAR NOT NULL,
    birthday   DATE    NOT NULL,
    department VARCHAR NOT NULL
);

CREATE TABLE inout
(
    employee_id INT     NOT NULL,
    event_date  DATE    NOT NULL,
    weekday     VARCHAR NOT NULL,
    event_time  TIME    NOT NULL,
    event_type  INT     NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE
);

INSERT INTO employees (full_name, birthday, department)
VALUES ('Ивахненко Дмитрий Александрович', '2001-11-22', 'ИТ'),
       ('Куров Андрей Владимирович', '1900-01-11', 'Бухгалтерия'),
       ('Владос Владосович ХХХ', '2000-03-04', 'Клининг'),
       ('Мазур Екатерина Алексеевна', '2000-11-06', 'ГлавБух');

INSERT INTO inout (employee_id, event_date, weekday, event_time, event_type)
VALUES (1, '2021-12-18', 'Суббота', '9:00', 1),
       (1, '2021-12-18', 'Суббота', '9:20', 2),
       (1, '2021-12-18', 'Суббота', '9:25', 1),
       (2, '2021-12-14', 'Суббота', '9:05', 1),
       (4, '2021-12-18', 'Суббота', '9:07', 1);

CREATE OR REPLACE FUNCTION get_truants(day DATE)
    RETURNS TABLE
            (
                full_name VARCHAR,
                departure VARCHAR
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT emp.full_name, emp.department
        FROM employees emp
        WHERE emp.full_name NOT IN (
            SELECT DISTINCT e.full_name
            FROM employees e
                     JOIN inout i ON e.id = i.employee_id
            WHERE i.event_date = day
              AND i.event_type = 1
        );
END;
$$ LANGUAGE PLPGSQL;

SELECT *
FROM get_truants('2021-12-18');



-- 1 --------------------------
-- Учитываем, что должен быть обязательно первый приход, так как если пришел на работу в 9-00, и тут же
-- вышел покурить, то значит, не опоздал.
-- Можно и через мин было сделать наверное, но это первое в голову пришло...
select distinct full_name
from (select e.full_name,
             i.event_time,
             row_number() over (partition by e.id order by i.event_time) as rn
      from employees e
               join inout i on e.id = i.employee_id
      where i.event_date = '2021-12-18'
        and i.event_type = 1) as late
where rn = 1
  and DATE_PART('minute', event_time::TIME - '9:00'::TIME) < 5
  and DATE_PART('minute', event_time::TIME - '9:00'::TIME) > 0;


--------- 2.
SELECT DISTINCT e.full_name
FROM employees e
         JOIN inout i ON e.id = i.employee_id
WHERE i.event_date = '2021-12-18'
  AND i.event_type = 2
  AND i.event_time - LAG(i.event_time) OVER (PARTITION BY i.event_time) > 10;


--------- 3.
SELECT DISTINCT e.full_name, e.department
FROM employees e
         JOIN inout i on e.id = i.employee_id
WHERE e.department = 'Бухгалтерия'
  AND i.event_type = 1
  AND i.event_time < '8:00'::TIME;