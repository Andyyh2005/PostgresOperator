import psycopg2

try:
    connect_str = "dbname='testpython' user='andy' host='localhost' " + \
                  "password='Sapvora123!'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()

    #cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
        (99, "xiaomi"))
    cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
        (120, "apple"))
    cursor.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
        (56, "sony"))
    #cursor.execute("DELETE FROM test WHERE id = (%s)", (2,))
    #cursor.execute("DROP TABLE test")

    conn.commit() # <--- makes sure the change is shown in the database

    cursor.execute("SELECT * FROM test;")
    rows = cursor.fetchall()
    print(rows)
    cursor.close()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)