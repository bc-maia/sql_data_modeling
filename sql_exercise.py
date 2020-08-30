import psycopg2
import pprint as pp


def test_connection_0():
    conn = psycopg2.connect(
        "host='localhost' dbname='test' user='postgres' password='passwd123'"
    )

    print("test conn 00: open")
    cursor = conn.cursor()

    # cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

    cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

    cursor.execute("SELECT * FROM public.test;")

    pp.pprint(cursor.fetchall())

    conn.commit()

    print("test conn 00: close")

    cursor.close()

    conn.close()


def test_connection_1():
    conn = psycopg2.connect(
        "host='localhost' dbname='test' user='postgres' password='passwd123'"
    )

    print("test conn 01: open")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS table2;")

    cursor.execute(
        """
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        completed BOOLEAN NOT NULL DEFAULT False
    );
    """
    )

    cursor.execute("INSERT INTO table2 (id, completed) VALUES (%s, %s);", (1, True))

    SQL = "INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);"
    data = {"id": 2, "completed": False}
    cursor.execute(SQL, data)

    conn.commit()

    print("test conn 01: close")
    conn.close()
    cursor.close()


if __name__ == "__main__":
    test_connection_0()
    test_connection_1()
