import os
import time

# find naem of sensor file
def sensor_name():
    f = open("../data/sensorname.txt", 'r')
    s = f.readline()
    temp_sensor = "/sys/bus/w1/devices/" + s.strip('\n') + "/w1_slave"
    f.close()
    return temp_sensor

# read raw sensor data
def temp_raw():
    temp_sensor = sensor_name()
    f = open(temp_sensor,'r')
    lines = f.readlines()
    f.close()
    return lines

# calculate temperature
def read_temp():
    lines = temp_raw()
    while (lines[0].strip()[-3:]!="YES"):
        time.sleep(0.2)
        lines = temp_raw()
    
    temp_output = lines[1].find('t=')

    if(temp_output != -1):
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string)/1000.0
        
    return temp_c # retrun celcius

def write_temp(temp):
    f = open("../data/temperature.txt", 'w')
    f.write(str(temp))
    f.close

if __name__ == "__main__":
    while(True):
        temp = read_temp()
        print(temp)
        time.sleep(1)
        write_temp(temp)
