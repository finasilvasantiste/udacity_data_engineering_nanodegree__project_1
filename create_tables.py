import psycopg2
from sql_queries import create_table_queries, drop_table_queries
import sqlalchemy as db


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    # connect to default database
    # engine = db.create_engine('postgresql://student:student@localhost/studentdb')
    # # cnx = engine.connect()

    conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student password=student")
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # create sparkify database with UTF8 encoding
    # db_name = 'sparkify'
    # with engine.connect() as conn:
    #     # Do not substitute user-supplied database names here.
    #     conn.execute(f"DROP DATABASE IF EXISTS {db_name}")
    #     conn.execute(f"CREATE DATABASE {db_name} WITH ENCODING 'utf8' TEMPLATE template0")

    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    print('DROP TABLES')
    print(len(drop_table_queries))
    for query in drop_table_queries:
        print('QUERY')
        print(query)
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
    # print('testing')
    # test_connection()
    # create_database()