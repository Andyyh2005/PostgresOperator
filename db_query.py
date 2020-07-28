import re
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
             callback("select * FROM test")

        class config:
            dbName = 'testpython'
            user = 'andy'
            host = 'localhost'
            password = 'testme'
            delimiter = ','
            outInbatch = True
            outbatchsize = 2


dbname = api.config.dbName
user = api.config.user
host = api.config.host
password = api.config.password
delimiter = api.config.delimiter # Delimiter to separate postrgres columns in output
outInbatch = api.config.outInbatch
outbatchsize = api.config.outbatchsize


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

        outStr = ""
        rows = []
        if not outInbatch:
            rows = cursor.fetchall()
            for r in rows:
                for i, c in enumerate(r):
                    outStr += str(c) + \
                        ('' if i==len(r)-1 else delimiter)
                outStr += "\n"
            api.send("output", outStr)
        else:
            rows = cursor.fetchmany(outbatchsize)
            while(rows):
                for r in rows:
                    for i, c in enumerate(r):
                        outStr += str(c) + \
                            ('' if i==len(r)-1 else delimiter)
                    outStr += "\n"
                api.send("output", outStr)
                outStr = ""
                rows = cursor.fetchmany(outbatchsize)
    except Exception as e:
        api.send("debug", str(e))
    finally:
        if(cursor):
            cursor.close()
        if(conn):
            conn.close()


# Interface for integrating the postgres query function into the pipeline engine
def on_input(data):
    if data:
        m = re.match(r'\s*select', data, flags=re.IGNORECASE)
        if m:
            handle_query(data)
        else:
            api.send("debug", "Only support SELECT Statement.")
    else:
        api.send("debug", "Input is empty.")


# Triggers the request for every message (the message provides the query)
api.set_port_callback("input", on_input)