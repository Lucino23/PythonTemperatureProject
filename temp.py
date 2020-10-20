import os
import glob
import time

# Activate the temperature sensors modules
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Define list to store the file names and one to store the temperatures from the sensor
file_list = []
temp_list = []

# Define the directory of the sensors
base_dir = '/sys/bus/w1/devices/'

# Read the raw temperature data out of the file
def read_temp_raw(device_file):
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

# Read the temperature from the raw data
def read_temp(device_file):
	lines = read_temp_raw(device_file)

	# Check if there is a valid checksum,
	# if there is it will be displayed with 'YES'
	# if there isn't a valid checksum
	# the function read_temp_raw() has to called
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw(device_file)

	# Search for 't=' on lines[1]
	t_pos = lines[1].find('t=')

	# If the string 't=' isn't present on lines[1]
	# it will return -1 otherwise it will return the position
	if t_pos != -1:
		temp_string = lines[1][t_pos+2:]
		temp = float(temp_string) / 1000.0
		return temp

# Fill the list with the file of each sensor
for device_folder in glob.glob(base_dir + '10*'):
        device_file = device_folder + '/w1_slave'
        file_list.append(device_file)

# Print the temperature of each sensor
while True:
	for sensor in file_list:
		temp_list.append(read_temp(device_file))
	print(temp_list)
	temp_list = []
	time.sleep(0.5)
