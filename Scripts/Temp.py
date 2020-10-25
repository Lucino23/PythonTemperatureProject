import os
import glob
import time
import sys
import mariadb

# Activate the temperature sensors modules
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Read the raw temperature data out of the file
def read_temp_raw(device_file):
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

# Read the temperature from the raw data
def read_temp(file):
        lines = read_temp_raw(file)

        # Check if there is a valid checksum,
        # if there is it will be displayed with 'YES'
        # if there isn't a valid checksum
        # the function read_temp_raw() has to called
        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw(file)

        # Search for 't=' on lines[1]
        t_pos = lines[1].find('t=')

        # If the string 't=' isn't present on lines[1]
        # it will return -1 otherwise it will return the position
        if t_pos != -1:
                temp_string = lines[1][t_pos+2:]
                temp = float(temp_string) / 1000.0
                return temp

# Get the last "Meting_id" from the "Meting" table
def get_last_Meting_id(cursor):
        query = """SELECT MAX(Meting_id) FROM Meting;"""
        cursor.execute(query)
        return cursor.fetchall()

# Get the Stop_datum_tijd from the last entry in the "Meting" table
def get_Stop_datum_tijd(cursor, Meting_id):
        query = """SELECT Stop_datum_tijd FROM Meting WHERE Meting_id = ?;"""
        cursor.execute(query, Meting_id)
        return cursor.fetchall()

# Calculate the average temperature
def Update_database(cursor, Meting_id, tempList):
        query  = """INSERT INTO Metingen(Sensor_1, Sensor_2, Sensor_3, Sensor_4, Meting_id) VALUES(?,?,?,?,?)"""
        data =  (tempList[0], tempList[1], tempList[2], tempList[3], Meting_id)
        cursor.execute(query, data)

# Main Function
def main():
        # Define lists to store each sensor it's file path and it's temperature
        files = []

        # Define tyhe list with default NULL as value because if a sensor didn't get a value we will have to insert null into the database
        temp_list = ["NULL", "NULL", "NULL", "NULL"]

        # Fill the list with the file of each sensor
        for device_folder in glob.glob('/sys/bus/w1/devices/10*'):
                device_file = device_folder + '/w1_slave'
                files.append(device_file)

        # Start the database connection
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

        # Create a variable to access the database with and get the last Meting_id and it's Stop_date_time        
        cursor = conn.cursor()
        conn.autocommit = True
        Meting_id = get_last_Meting_id(cursor)
        Stop_datum_tijd = get_Stop_datum_tijd(cursor, Meting_id)

        # Get the temperature of each sensor and update the database table "Metingen"
        while Stop_datum_tijd == "NULL":
                for i in range(len(files)):
                        temp_list[i] = read_temp(files[i])
                Update_database(cursor, Meting_id, temp_list)
                Stop_datum_tijd = get_Stop_datum_tijd(cursor, Meting_id)
                temp_list = ["NULL", "NULL", "NULL", "NULL"]
                time.sleep(2)

        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()