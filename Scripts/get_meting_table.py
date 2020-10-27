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

# Insert the data in to the "Meting" table
query = """SELECT * FROM Meting;"""
cursor.execute(query)
db_data = cursor.fetchall()

# Close the database connection
conn.close()
