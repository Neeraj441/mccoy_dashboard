import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(host='34.134.150.30',
                                   user='root',
                                   password='instance2',
                                   database='mccoy_energy')
    if conn.is_connected():
        db_Info = conn.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        cursor.execute("SELECT * FROM SM_Weather")

        table_results = cursor.fetchall()

        for x in table_results:
            print(x)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection is closed")
