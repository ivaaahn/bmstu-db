create table if not exists empl_visits
(
    department VARCHAR,
    fio        VARCHAR,
    date_      DATE,
    status     VARCHAR
);



insert into empl_visits (department, fio, date_, status)
values ('ИТ', 'Иванов Иван Иванович', '2020-01-15', 'Больничный'),
       ('ИТ', 'Иванов Иван Иванович', '2020-01-16', 'На работе'),
       ('ИТ', 'Иванов Иван Иванович', '2020-01-17', 'На работе'),
       ('ИТ', 'Иванов Иван Иванович', '2020-01-18', 'На работе'),
       ('ИТ', 'Иванов Иван Иванович', '2020-01-19', 'Оплачиваемый отпуск'),
       ('ИТ', 'Иванов Иван Иванович', '2020-01-20', 'Оплачиваемый отпуск'),
       ('Бухгалтерия', 'Петрова Ирина Ивановна', '2020-01-15', 'Оплачиваемый отпуск'),
       ('Бухгалтерия', 'Петрова Ирина Ивановна', '2020-01-16', 'На работе'),
       ('Бухгалтерия', 'Петрова Ирина Ивановна', '2020-01-17', 'На работе'),
       ('Бухгалтерия', 'Петрова Ирина Ивановна', '2020-01-18', 'На работе'),
       ('Бухгалтерия', 'Петрова Ирина Ивановна', '2020-01-19', 'Оплачиваемый отпуск'),
       ('Бухгалтерия', 'Петрова Ирина Ивановна', '2020-01-20', 'Оплачиваемый отпуск');


with ext_empl_visits as (
    select row_number() over (partition by ev.fio, ev.status order by ev.date_) as idx,
           ev.fio,
           ev.status,
           ev.date_
    from empl_visits ev
)
select eev.fio,
       eev.status,
       min(eev.date_) as date_from,
       max(eev.date_) as date_to
from ext_empl_visits eev
group by eev.fio, eev.status, eev.date_ - make_interval(days=>idx::int)
order by eev.fio, date_from;