from models import *

LINQ_TO_JSON_DESCR = {
    6: ('Получить имя', None),
    7: ('Обновить', None),
    8: ('Добавить', None),
}

LINQ_TO_JSON_QUERIES = {
    6: [
        ["first_name", "last_name"],
        [
            [row.first_name] for row in
            Employees_JSONB.select(
                Employees_JSONB.data["name"]["first"].alias("first_name"),
                Employees_JSONB.data["name"]["last"].alias("last_name"),
            )
        ]
    ],
    7: Employees_JSONB.update(
        {
            Employees_JSONB.data: Employees_JSONB.data.concat(
                {"age": 20}
            )
        }
    ),
    8: Employees_JSONB.insert(
        data={
            "id": 3,
            "age": 27,
            "name": {
                "last": "Ivanov",
                "first": "Ivan",
            },
            "address": {
                "city": "St. Petersburg",
                "country": "Russia",
            }
        }
    )
}
