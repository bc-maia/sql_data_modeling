from pprint import pprint
from sqlalchemy import engine

engine = engine.create_engine("postgresql://postgres:passwd123@localhost:5432/test")

connection = engine.connect()

result = connection.execute("SELECT * FROM persons")

for row in result:
    pprint(row)

result.close()
connection.close()

print("closed connection")