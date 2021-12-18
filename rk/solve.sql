drop database if exists rk2;
create database rk2;

create table employee
(
    id         serial primary key,
    full_name  varchar,
    birth_year int,
    experience int,
    phone      varchar
);


create table employee_duty
(
    employee_id int,
    duty_id     int,
    foreign key (employee_id) references employee (id) on delete cascade,
    foreign key (duty_id) references duty (id) on delete cascade
);

create table duty
(
    id         serial primary key,
    duty_date  date,
    work_hours int
);

create table security_post
(
    id          serial primary key,
    name        varchar,
    address     varchar,
    employee_id int,
    foreign key (employee_id) references employee (id) on delete cascade
);


INSERT INTO employee (full_name, birth_year, experience, phone)
VALUES ('Sergey', 2000, 1, '+7-907-555-6505'),
       ('Pasha', 2000, 3, '+7-909-555-3636'),
       ('Lyosha', 2000, 4, '+7-902-555-1483'),
       ('Dima', 2000, 1, '+7-909-555-8364'),
       ('Artem', 2000, 5, '+7-925-553-0044'),
       ('Igor', 2000, 3, '+7-951-555-3321'),
       ('Maxim', 2000, 1, '+7-951-555-8033'),
       ('Sasha', 2000, 8, '+7-908-555-0847'),
       ('Ed', 2000, 2, '+7-952-555-7675'),
       ('John', 2000, 4, '+7-952-555-1784');


INSERT INTO duty (duty_date, work_hours)
VALUES ('2020-05-01', 5),
       ('2020-05-02', 5),
       ('2020-05-03', 5),
       ('2020-05-04', 5),
       ('2020-06-01', 5),
       ('2020-06-02', 5),
       ('2020-06-03', 5),
       ('2020-07-03', 5),
       ('2020-08-03', 5),
       ('2020-09-03', 5);


INSERT INTO employee_duty (employee_id, duty_id)
VALUES (1, 1),
       (1, 2),
       (1, 3),
       (2, 2),
       (2, 3),
       (2, 4),
       (3, 4),
       (4, 4),
       (5, 5),
       (6, 5),
       (7, 5);



INSERT INTO security_post (name, address, employee_id)
values ('Пост1', 'Адрес1', 1),
       ('Пост2', 'Адрес2', 2),
       ('Пост3', 'Адрес3', 3),
       ('Пост4', 'Адрес4', 1),
       ('Пост5', 'Адрес5', 4),
       ('Пост6', 'Адрес6', 5),
       ('Пост7', 'Адрес7', 6),
       ('Пост8', 'Адрес8', 7),
       ('Пост9', 'Адрес9', 8),
       ('Пост10', 'Адрес10', 9),
       ('Пост11', 'Адрес11', 10);



-- Инструкция SELECT, использующая предикат IN с вложенным подзапросом.
-- Получить имена всех работников, которые дежурили в пятом месяце...
select full_name
from employee
         join employee_duty ed on employee.id = ed.employee_id
where employee.id in (select id from duty d where extract(month from d.duty_date) = 5);



-- Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов
-- Для каждого дежурства находит средний и максимальный опыт сотрудника смены.
select d.id,
       d.duty_date,
       (select avg(experience)
        from employee_duty
                 join employee e on e.id = employee_duty.employee_id
        where duty_id = d.id) as avg_empl_experience,
       (select max(experience)
        from employee_duty
                 join employee e on e.id = employee_duty.employee_id
        where duty_id = d.id) as max_empl_experience
from employee_duty ed
         join duty d on ed.duty_id = d.id;


-- Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3.
-- Получить список сотрудников, которые заступали на максимальное число дежурств
select *
from employee e
where e.id in (select ed.employee_id
               from employee_duty ed
               group by ed.employee_id
               having count(distinct duty_id) = (select max(cnt)
                                                 from (select ed.employee_id, count(distinct ed.duty_id) as cnt
                                                       from employee_duty ed
                                                       group by ed.employee_id) as tmp)
);


-- 3
-- Процедура, которая удаляет все вьюхи из паблик схемы (шифрования в постгре нет...)
create or replace procedure delete_views() as
$$
declare
    elem varchar = '';
begin
    for elem in execute 'select table_name from information_schema.views where table_schema = ''public'''
        loop
            execute 'DROP VIEW ' || elem;
        end loop;

end;
$$ language plpgsql;


-- Тестовые вьюхи для задания3
create view test_view1 as
select *
from duty;

create view test_view2 as
select *
from employee;

create view test_view3 as
select *
from employee_duty;

create view test_view4 as
select *
from security_post;


-- Удалить вьюхи
call delete_views();


-- Получить вьюхи
select table_name
from information_schema.views
where table_schema = 'public';


create table C
(
    id serial primary key
);


create table P1
(
    id       serial primary key,
    child_id int,
    foreign key (child_id) references C (id) on delete cascade
);

create table P2
(
    id       serial primary key,
    child_id int,
    foreign key (child_id) references C (id) on delete cascade
);


select c.id
from C
         inner join P1 on C.id = P1.child_id
         inner join P2 on C.id = P2.child_id





