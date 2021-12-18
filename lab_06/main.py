import asyncio
import os

from lab_06.config import setup_config
from lab_06.db import setup_connection


async def main():
    conn = await setup_connection(setup_config(os.environ.get("CONFIG_L6")))

    values = await conn.fetch(
        'SELECT * FROM customers WHERE id = $1', 10,
    )

    res = await conn.execute(
        'INSERT INTO customers(id, first_name, last_name, email, phone_number) VALUES '
        '($1, $2, $3, $4, $5);', 1001, "Test", "Test", "test@mail.ru", "88005553535"
    )

    print(values)
    print(res)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
