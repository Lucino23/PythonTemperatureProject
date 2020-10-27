import sys
from datetime import datetime
import mariadb

# Start the connection
try:
    conn = mariadb.connect(
    user="luca",
    password="Antluc0824",
    host="localhost",
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

# Get all the data from the "Metingen" table
query = """SELECT AVG(Sensor_1), AVG(Sensor_2), AVG(Sensor_3), AVG(Sensor_4), AVG(AVG(Sensor_1) + AVG(Sensor_2) + AVG(Sensor_3) + AVG(Sensor_4)) FROM Metingen WHERE Meting_id = ?;"""
cursor.execute(query, Meting_id)
db_data = cursor.fetchall()

# Update the data in to the "Meting" table
query = """UPDATE Meting SET Stop_datum_tijd = ?, Avg_S1 = ?, Avg_S2 = ?, Avg_S3 = ?, Avg_S4 = ?, Average = ?) WHERE Meting_id = ?;"""
data = (datetime.now(), db_data[0], db_data[1], db_data[2], db_data[3], db_data[4], Meting_id)
cursor.execute(query, data)

# Close the database connection
conn.close()
