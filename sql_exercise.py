import psycopg2
import pprint as pp


def test_connection()
    conn = psycopg2.connect(
        "host='localhost' dbname='test' user='postgres' password='passwd123'"
    )

    print("conn open")
    cursor = conn.cursor()

    # cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

    cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

    cursor.execute("SELECT * FROM public.test;")

    pp.pprint(cursor.fetchall())

    conn.commit()

    print("conn close")

    cursor.close()

    conn.close()
    

if __name__ == "__main__":
    test_connection()