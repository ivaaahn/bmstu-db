from pprint import pprint

from db import db
from models import Employees

from .linq_to_object import (
    LINQ_TO_OBJECT_QUERIES as ltoobjq,
    LINQ_TO_OBJECT_DESCR as ltoobjdescr,
)

LINQ_TO_SQL_DESCR = {
    9: ltoobjdescr[2],
    10: ltoobjdescr[3],
    11: (
        'Добавить еще одного рабочего',
        '''
        insert into employees 
        values ('Дмитрий', 'Ивахненко', '2022-01-01', '2001-11-22', 5.0, 99999, 'ivaaahn@gmail.com', '+79510755706')
        '''
    ),
    12: (
        'Повысить зарплату новому рабочему',
        '''
        update employees set salary = 1000000000 where id = 1001; 
        '''
    ),
    13: (
        'Удалить нового рабочего',
        '''
        delete from employees where id = 1001; 
        '''
    ),
    14: (
        'Получить расширенную информацию о заказах',
        '''
        select * from ext_orders_info();
        '''
    ),
}


def fetch_ext_orders_info():
    cur = db.cursor()
    cur.callproc('ext_orders_info')
    pprint(cur.fetchall())
    cur.close()


LINQ_TO_SQL_QUERIES = {
    9: ltoobjq[2],
    10: ltoobjq[3],
    11: Employees.insert(
        id=1001,
        first_name='Дмитрий',
        last_name='Ивахненко',
        employed_since='2022-01-01',
        birthdate='2001-11-22',
        rating=5.0,
        salary=99999,
        email='ivaaahn@gmail.com',
        phone_number='+79510755706',
    ),
    12: Employees.update(salary=1000000000).where(Employees.id == 1001),
    13: Employees.delete().where(Employees.id == 1001),
    14: fetch_ext_orders_info,
}
