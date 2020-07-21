# Mock pipeline engine api to allow testing outside pipeline engine
try:
    api
except NameError:
    class api:
        @staticmethod
        def send(port, data):
             print(port + " receieved: " + str(data))

        @staticmethod   
        def set_port_callback(port, callback):
             print(
                 "Call \"" + callback.__name__ + "\" to simulate behavior when messages arrive at port \"" + port + "\"..")
             callback()

        class config:
            # connect_str = "dbname='testpython' user='andy' host='localhost' " + "password='Sapvora123!'"
            dbname = 'testpython'
            user = 'andy'
            host = 'localhost'
            password = 'Sapvora123!'
            api.config.delimiter = ','

try:
    import psycopg2
except:
    raise ValueError("psycopg2 library is not installed. Run 'pip install psycopg2' for installing it.\n")

if api.config.dbname == "":
    raise ValueError("The dbname config cannot be empty.")

if api.config.user == "":
    raise ValueError("The user config field cannot be empty.")

if api.config.password == "":
    raise ValueError("The password config field cannot be empty.")

if api.config.host == "":
    raise ValueError("The host config field cannot be empty.")


def on_input(inSql):
    try:
        # Connect to an existing database
        connect_str = "dbname=" + api.config.dbname + " " + "user=" + api.config.user + " " + "host=" + api.config.host + " " + \
            "password=" + api.config.password
        #"dbname='testpython' user='andy' host='localhost' " + \
        #              "password='Sapvora123!'"
        conn = psycopg2.connect(connect_str)
        
        # Open a cursor to perform database operations
        cur = conn.cursor()
        
        cur.execute(inSql)
        conn.commit()
        
        # Execute a command: this creates a new table
        # cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        
        # Pass data to fill a query placeholders and let Psycopg perform the correct conversion (no more SQL injections!)
        # cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))

        # Query the database and obtain data as Python objects
        #cur.execute("SELECT * FROM test;")
       
        rows = cur.fetchall()
        cur.close()
        conn.close()

        outStr = ""
        for r in rows:
            for c in r:
                outStr = outStr + str(c) + ','#api.config.delimiter ## Delimiter to separate postrgres columns in output
            outStr += "\n"
              
        api.send("output", outStr)
    except Exception as e:
        api.send("debug", "Can't connect. Invalid dbname, user or password?")
        api.send("debug", e)


# Interface for integrating the postgres query function into the pipeline engine
def interface():
    sql = 'SELECT * FROM test WHERE id > 1 ORDER BY id ASC LIMIT 1'

    try:
        on_input(sql)
    except Exception as excp:
        api.send("debug", excp)


api.set_port_callback("inSql", interface)