import sys
from datetime import datetime
import mariadb

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
query = """INSERT INTO Meting(Start_datum_tijd, Stop_datum_tijd, Avg_S1, Avg_S2, Avg_S3, Avg_S4, Average) VALUES(?,?,?,?,?,?,?);"""
data = (datetime.now(), "NULL", "NULL", "NULL", "NULL", "NULL", "NULL")
cursor.execute(query, data)
conn.close()