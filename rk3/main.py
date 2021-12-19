# ВАРИАНТ НОМЕР Ч Е Т Ы Р Е !!!!!

import peewee as pw
from playhouse.db_url import connect

db = connect("postgresext://labs:labs@localhost:5432/mct3")


class BaseModel(pw.Model):
    class Meta:
        database = db


class Employees(BaseModel):
    id = pw.PrimaryKeyField()
    full_name = pw.CharField()
    birthday = pw.DateField()
    department = pw.CharField()


class Inout(BaseModel):
    employee_id = pw.ForeignKeyField(Employees, on_delete="cascade")
    event_date = pw.DateField()
    event_delay = pw.CharField()
    event_time = pw.TimeField()
    event_type = pw.IntegerField()


def t1():
    query = '''
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
  '''

    cursor = db.execute_sql(query)

    for row in cursor.fetchall():
        print(row)

    subquery = (
        Employees.select(
            Employees.full_name,
            Inout.event_time,
            pw.fn.row_number().over(partition_by=Employees.id, order_by=[Inout.event_time])
        ).join(Inout).where(Inout.event_type == 1 & Inout.event_date == '2021-12-18')
    )

    cursor = Employees.select(subquery.full_name).join(
    ).where(pw.fn.Date_part('minute', Inout.evtime.cast("time") - pw.Cast("9:00", "time")))

    for row in cursor:
        print(row)


def t2():
    query = '''
    SELECT DISTINCT e.full_name
FROM employees e
         JOIN inout i ON e.id = i.employee_id
WHERE i.event_date = '2021-12-18'
  AND i.event_type = 2
  AND i.event_time - LAG(i.event_time) OVER (PARTITION BY i.event_time) > 10;
  '''

    cursor = db.execute_sql(query)

    for row in cursor.fetchall():
        print(row)

    cursor = Employees.select(Employees.fio).join(Inout).where(
        Inout.evdate == "2021-12-18"
        & Inout.evtype == 2
        & (Inout.evtime - pw.fn.Lag(Inout.evtime).over(partition_by=[Inout.evtime]) > 10))

    for row in cursor:
        print(row)


def t3():
    query = '''
    SELECT DISTINCT e.full_name, e.department
FROM employees e
         JOIN inout i on e.id = i.employee_id
WHERE e.department = 'Бухгалтерия'
  AND i.event_type = 1
  AND i.event_time < '8:00'::TIME;
  '''

    cursor = db.execute_sql(query)
    for row in cursor.fetchall():
        print(row)

    cursor = Employees.select(Employees.full_name, Employees.department).join(Inout).where(
        Employees.department == "Бухгалтерия" &
        Inout.event_type == 1 &
        Inout.event_time < pw.Cast("8:00", "time")
    )

    for row in cursor:
        print(row)


def main():
    t1()
    t2()
    t3()


if __name__ == "__main__":
    main()
