drop table if exists employees2;

create table employees2
(
    "id"             SERIAL PRIMARY KEY,
    "first_name"     varchar        NOT NULL,
    "last_name"      varchar        NOT NULL,
    "employed_since" date           NOT NULL,
    "birthdate"      date,
    "rating"         float          NOT NULL check ( rating >= 0.0 AND rating <= 5.0 ),
    "salary"         float          NOT NULL check ( salary >= 0.0 ),
    "email"          varchar UNIQUE,
    "phone_number"   varchar UNIQUE NOT NULL
);

create temp table temp_json
(
    data jsonb
);

\copy temp_json(data) from 'json/employees.json';

insert into employees2
select (data ->> 'id')::int,
       data ->> 'first_name',
       data ->> 'last_name',
       (data ->> 'employed_since')::date,
       (data ->> 'birthdate')::date,
       (data ->> 'rating')::float,
       (data ->> 'salary')::float,
       data ->> 'email',
       data ->> 'phone_number'
from temp_json;