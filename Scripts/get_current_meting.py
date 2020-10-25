import sys
from datetime import datetime
import mariadb

# Get the Stop_datum_tijd from the last entry in the "Meting" table
def get_Stop_datum_tijd(cursor, Meting_id):
    query = """SELECT Stop_datum_tijd FROM Meting WHERE Meting_id = ?;"""
    cursor.execute(query, Meting_id)
    return cursor.fetchall()

# Start the connection
try:
    conn = mariadb.connect(
    user="luca",
    password="Antluc0824",
    host="192.168.0.118",
    port=3306,
    database="PyTempProject"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Create an entry in the "Meting" table
cursor = conn.cursor()
conn.autocommit = True

# Get the last Meting_id from the "Meting" table
query = """SELECT MAX(Meting_id) FROM Meting;"""
cursor.execute(query)
Meting_id = cursor.fetchall()

Stop_datum_tijd = get_Stop_datum_tijd(cursor, Meting_id)

while Stop_datum_tijd != "NULL":
    # Get the  the data in to the "Meting" table
    query = """SELECT Sensor_1, Sensor_2, Sensor_3, Sensor_4 FROM Metingen WHERE Meting_id = ? and Metingen_id = MAX(Metingen_id);"""
    cursor.execute(query, Meting_id)
    db_data = cursor.fetchall()

    # Check if stop has been pressed by checking if Stop_datum_time is not null
    Stop_datum_tijd = get_Stop_datum_tijd(cursor, Meting_id)

# Close the database connection
conn.close()