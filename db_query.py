import psycopg2


def handle_query(inSql):
    conn = None
    cur = None
    try:
        # Connect to an existing database
        connect_str = "dbname=" + api.config.dbname + " " + \
            "user=" + api.config.user + " " + \
            "host=" + api.config.host + " " + \
            "password=" + api.config.password
        conn = psycopg2.connect(connect_str)
    except Exception as e:
        raise e
        
    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    try:
        cur.execute(inSql)
    except Exception as e:
        cur.close()
        raise e

    conn.commit()
        
    try:
        outStr = ""
        rows = cur.fetchmany(2)
        while(rows):
            for r in rows:
                for i, c in enumerate(r):
                    outStr += str(c) + \
                    ('' if i==len(r)-1 else api.config.delimiter) # Delimiter to separate postrgres columns in output
                outStr += "\n"
            api.send("output", outStr)
            outStr = ""
            rows = cur.fetchmany(2)
    except Exception as e:
        cur.close()
        conn.close()
        raise e
    
    cur.close()
    conn.close()


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
             callback()

        class config:
            dbname = 'testpython'
            user = 'andy'
            host = 'localhost'
            password = 'Sapvora123!'#TODO: change to XX
            delimiter = ','
            query = 'SELECT * FROM test'


# Interface for integrating the postgres query function into the pipeline engine
def interface():
    sql = api.config.query

    try:
        handle_query(sql)
    except Exception as excp:
        api.send("debug", str(excp))


# Triggers the request for every message (the message provides the query)
api.set_port_callback("inSql", interface)