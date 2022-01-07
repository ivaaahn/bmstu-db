from playhouse.db_url import connect
import os

db = connect(
    f'postgresext://{os.getenv("BMSTU_USER")}:{os.getenv("BMSTU_PSWD")}@localhost:5432/{os.getenv("BMSTU_DB")}'
)
