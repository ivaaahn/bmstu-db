drop table if exists employees_jsonb;

create table employees_jsonb (
    data jsonb
);

insert into employees_jsonb(data) values
('{"id":858,"name": {"first":"Аникей","last":"Зиновьев"},"employed_since":"2019-02-22","birthdate":"1998-03-29","rating":3.4,"salary":25070,"email":"bmoormannt@google.cn","phone_number":"+86 (154) 536-5907"}'),
('{"id":859,"name": {"first":"Харитон","last":"Дмитриев"},"employed_since":"2019-03-07","birthdate":"1995-12-20","rating":4.9,"salary":24738,"email":"wtamplinnu@lulu.com","phone_number":"+86 (811) 316-2168"}'),
('{"id":860,"name": {"first":"Лидия","last":"Кузьмина"},"employed_since":"2016-01-25","birthdate":"1972-03-31","rating":3.7,"salary":29220,"email":"csmissennv@netscape.com","phone_number":"+81 (892) 244-6740"}');



select data->'id' as id, data->'employed_since' as employed_since
from employees_jsonb;

--

select data->'id' as id, data->'name'->'first' as country
from employees_jsonb;

--

create function key_exists(data jsonb, key varchar)
returns boolean
language plpgsql
as
$$
begin
    return (data->key) is not null;
end;
$$;

select key_exists(e.data, 'blah')
from employees_jsonb e;

--

update employees_jsonb
set data = data || '{ "address": { "country": "Russia", "city": "Kursk" } }'::jsonb
where (data->>'id')::int = 858;

--

create temp table employees_json (
    data json
);

insert into employees_json(data) values
('[{"id":858,"name": {"first":"Аникей","last":"Зиновьев"},"employed_since":"2019-02-22","birthdate":"1998-03-29","rating":3.4,"salary":25070,"email":"bmoormannt@google.cn","phone_number":"+86 (154) 536-5907"},
{"id":859,"name": {"first":"Харитон","last":"Дмитриев"},"employed_since":"2019-03-07","birthdate":"1995-12-20","rating":4.9,"salary":24738,"email":"wtamplinnu@lulu.com","phone_number":"+86 (811) 316-2168"},
{"id":860,"name": {"first":"Лидия","last":"Кузьмина"},"employed_since":"2016-01-25","birthdate":"1972-03-31","rating":3.7,"salary":29220,"email":"csmissennv@netscape.com","phone_number":"+81 (892) 244-6740"}]');


select jsonb_array_elements(data::jsonb)
from employees_json;