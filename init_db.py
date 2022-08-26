from config import database

conn = database.get_database_connection()

curr = conn.cursor()

curr.execute("DROP TABLE IF EXISTS staff;")

curr.execute(
    "CREATE TABLE staff (id serial PRIMARY KEY,"
    "name varchar (150) NOT NULL,"
    "email varchar (50) NOT NULL,"
    "phone_number integer NOT NULL,"
    "address text NOT NULL,"
    "password varchar (255) NOT NULL),"
    "is_admin boolean;"
)


conn.commit()

curr.close()
conn.close()
