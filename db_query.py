import psycopg2

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
                 "Call \"" + callback.__name__ + "\" to simulate behavior when messages arrive at port \"" + port + "\".")
             callback("SELECT * FROM test55")

        class config:
            dbname = 'testpython'
            user = 'andy'
            host = 'localhost'
            password = 'Sapvora123!'#TODO: change to XX
            delimiter = ','


dbname = api.config.dbname
user = api.config.user
host = api.config.host
password = api.config.password

def handle_query(query):
    conn = None
    cursor = None
    try:
        # Connect to an existing database
        connect_str = "dbname=" + dbname + " " + \
            "user=" + user + " " + \
            "host=" + host + " " + \
            "password=" + password
        conn = psycopg2.connect(connect_str)
        
        # Open a cursor to perform database operations
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

        # output the query result to the output port
        outStr = ""
        rows = cursor.fetchmany(2)
        while(rows):
            for r in rows:
                for i, c in enumerate(r):
                    outStr += str(c) + \
                    ('' if i==len(r)-1 else api.config.delimiter) # Delimiter to separate postrgres columns in output
                outStr += "\n"
            api.send("output", outStr)
            outStr = ""
            rows = cursor.fetchmany(2)
    except Exception as e:
        api.send("debug", str(e))
    finally:
        if(cursor):
            cursor.close()
        if(conn):
            conn.close()


# Interface for integrating the postgres query function into the pipeline engine
def interface(query):
    if query:
        handle_query(query)
    else:
        api.send("debug", "Input is empty")


# Triggers the request for every message (the message provides the query)
api.set_port_callback("input", interface)