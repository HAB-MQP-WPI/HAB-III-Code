#!/usr/bin/env python
fro#!/usr/bin/env python
from time import sleep
from threading import Thread
import time
import serial
import os
import glob
import ms5803py
import pynmeagps
from gpiozero import CPUTemperature

Arduino_sensor_data = ''
GPS_Sensor_data = ''

stream = serial.Serial('/dev/ttyUSB1',9600) #GPS Port

uno_port = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

radio_port =serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


nmr = pynmeagps.NMEAReader(stream)
cpu = CPUTemperature()
s = ms5803py.MS5803()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    if len(lines) >1:
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c

def read_GGA():
    for x in range(24):
        try:
            (raw_data, parsed_dat) = nmr.read()
            if parsed_dat.msgID =="GGA":
                GPSlat1 = 0
                GPSlong1 = 0
                GPSalt1 = 0
                if parsed_dat.quality >0:
                    GPSlat1 = parsed_dat.lat
                    GPSlong1 = parsed_dat.lon
                    GPSalt1 = parsed_dat.alt
                return parsed_dat.time, parsed_dat.numSV, GPSlat1, GPSlong1,GPSalt1
        except Exception as e:
            print(e)
    return 0,0,0,0,0

def arduino_sensors():
    print('arduino sensors\n')
    outF=open("HAB3SensorData.txt","w")
    outF.write('Start of Arduino Sensor Data\n')

    new_data = False
    global Arduino_sensor_data

    while 1:
        x=uno_port.readline()
        LOCtime = time.localtime()
        LOCtimeSTR = time.strftime("%m/%d/%Y %H:%M:%S", LOCtime)
        if (len(x) > 4):
            if (new_data == False):
                Arduino_sensor_data = ''
            Arduino_sensor_data = Arduino_sensor_data + str(x) + '\n'
            new_data = True
        else:
            new_data = False
        outF.close()
        outF=open("HAB3SensorData.txt",'a')
        outF.write(LOCtimeSTR+' '+str(x)+'\n')

def pi_sensors():
    global GPS_Sensor_data
    GPStime = ''
    GPSlat = 0
    GPSlong = 0
    GPSalt = 0
    GPSsats = 0
    wTemp = 0
    pTemp = 0
    pPres = 0
    print('pi_sensors')
    GPS_F=open("HAB3GPSData.txt","w")
    GPS_F.write('Start of GPS Data\n')
    while 1:
        GPStime,GPSsats,GPSlat,GPSlong,GPSalt = read_GGA()
        try:
            pPres, pTemp =s.read(pressure_osr=512);
        except Exception as e:
            print(e)
        CPUTemp = cpu.temperature
        LOCtime = time.localtime()
        LOCtimeSTR = time.strftime("%m/%d/%Y %H:%M:%S", LOCtime)
        wTemp = read_temp()

        if CPUTemp is None:
            CPUTemp = 0
        if wTemp is None:
            wTemp = 0
        if pTemp is None:
            pTemp = 0
        if GPSlat is None:
            GPSlat = 0
        if GPSlong is None:
            GPSLong = 0
        if GPSalt is None:
            GPSalt = 0
        if GPSsats is None:
            GPSsats = 0
        GPS_F.close()    
        GPS_F=open("HAB3GPSData.txt",'a')
        GPS_F.write(str("CPUtemp {:4.2f} wTemp {:4.2f} pTemp {:4.2f} pPres {} Time {} UTC {} Lat {:10.8f} Long {:10.8f} Altitude {:8.1f} #Sats {:2d}".format(CPUTemp,wTemp, pTemp,pPres,LOCtimeSTR,GPStime,GPSlat, GPSlong,GPSalt,GPSsats))+'\n')
        
        GPS_Sensor_data = str("PT: {:4.2f} C\nPP: {} mBar\nLAT: {:10.6f} \nLON: {:10.6f} \nALT: {:8.1f} m\n".format(wTemp,pPres,GPSlat,GPSlong,GPSalt))
        
        print(GPS_Sensor_data)
    
def transmit_data():
    global Arduino_sensor_data
    print('transmit_data')
    outF=open("HAB3RadioData.txt","w")
    outF.write('Start of Transmitted Radio Data\n')
    while 1:
        LOCtime = time.localtime()
        LOCtimeSTR = time.strftime("%m/%d/%Y %H:%M:%S", LOCtime)
        radio_port.write(bytes((str(Arduino_sensor_data)+GPS_Sensor_data), 'utf-8'))
        print (Arduino_sensor_data)
        outF.close()
        outF=open("HAB3RadioData.txt",'a')
        outF.write(LOCtimeSTR+' '+str(Arduino_sensor_data)+ GPS_Sensor_data +'\n')
        sleep(1)

# create two new threads
ardunio_thread = Thread(target=arduino_sensors)
pi_thread = Thread(target=pi_sensors)
transmit_thread = Thread(target=transmit_data)

# start the threads
ardunio_thread.start()
pi_thread.start()
transmit_thread.start()
m time import sleep
from threading import Thread
import time
import serial
import os
import glob
import ms5803py
import pynmeagps
from gpiozero import CPUTemperature

Arduino_sensor_data = ''
GPS_Sensor_data = ''

stream = serial.Serial('/dev/ttyUSB1',9600) #GPS Port

uno_port = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

radio_port =serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


nmr = pynmeagps.NMEAReader(stream)
cpu = CPUTemperature()
s = ms5803py.MS5803()

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    if len(lines) >1:
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            # temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c

def read_GGA():
    for x in range(24):
        try:
            (raw_data, parsed_dat) = nmr.read()
            if parsed_dat.msgID =="GGA":
                GPSlat1 = 0
                GPSlong1 = 0
                GPSalt1 = 0
                if parsed_dat.quality >0:
                    GPSlat1 = parsed_dat.lat
                    GPSlong1 = parsed_dat.lon
                    GPSalt1 = parsed_dat.alt
                return parsed_dat.time, parsed_dat.numSV, GPSlat1, GPSlong1,GPSalt1
        except Exception as e:
            print(e)
    return 0,0,0,0,0

def arduino_sensors():
    print('arduino sensors\n')
    outF=open("HAB3SensorData.txt","w")
    outF.write('Start of Arduino Sensor Data\n')

    new_data = False
    global Arduino_sensor_data

    while 1:
        x=uno_port.readline()
        LOCtime = time.localtime()
        LOCtimeSTR = time.strftime("%m/%d/%Y %H:%M:%S", LOCtime)
        if (len(x) > 4):
            if (new_data == False):
                Arduino_sensor_data = ''
            Arduino_sensor_data = Arduino_sensor_data + str(x) + '\n'
            new_data = True
        else:
            new_data = False
        outF.close()
        outF=open("HAB3SensorData.txt",'a')
        outF.write(LOCtimeSTR+' '+str(x)+'\n')

def pi_sensors():
    global GPS_Sensor_data
    GPStime = ''
    GPSlat = 0
    GPSlong = 0
    GPSalt = 0
    GPSsats = 0
    wTemp = 0
    pTemp = 0
    pPres = 0
    print('pi_sensors')
    GPS_F=open("HAB3GPSData.txt","w")
    GPS_F.write('Start of GPS Data\n')
    while 1:
        GPStime,GPSsats,GPSlat,GPSlong,GPSalt = read_GGA()
        try:
            pPres, pTemp =s.read(pressure_osr=512);
        except Exception as e:
            print(e)
        CPUTemp = cpu.temperature
        LOCtime = time.localtime()
        LOCtimeSTR = time.strftime("%m/%d/%Y %H:%M:%S", LOCtime)
        wTemp = read_temp()

        if CPUTemp is None:
            CPUTemp = 0
        if wTemp is None:
            wTemp = 0
        if pTemp is None:
            pTemp = 0
        if GPSlat is None:
            GPSlat = 0
        if GPSlong is None:
            GPSLong = 0
        if GPSalt is None:
            GPSalt = 0
        if GPSsats is None:
            GPSsats = 0
        GPS_F.close()    
        GPS_F=open("HAB3GPSData.txt",'a')
        GPS_F.write(str("CPUtemp {:4.2f} wTemp {:4.2f} pTemp {:4.2f} pPres {} Time {} UTC {} Lat {:10.8f} Long {:10.8f} Altitude {:8.1f} #Sats {:2d}".format(CPUTemp,wTemp, pTemp,pPres,LOCtimeSTR,GPStime,GPSlat, GPSlong,GPSalt,GPSsats))+'\n')
        
        GPS_Sensor_data = str("PT: {:4.2f} C\nPP: {} mBar\nLAT: {:10.6f} \nLON: {:10.6f} \nALT: {:8.1f} m\n".format(wTemp,pPres,GPSlat,GPSlong,GPSalt))
        
        print(GPS_Sensor_data)
    
def transmit_data():
    global Arduino_sensor_data
    print('transmit_data')
    outF=open("HAB3RadioData.txt","w")
    outF.write('Start of Transmitted Radio Data\n')
    while 1:
        LOCtime = time.localtime()
        LOCtimeSTR = time.strftime("%m/%d/%Y %H:%M:%S", LOCtime)
        radio_port.write(bytes((str(Arduino_sensor_data)+GPS_Sensor_data), 'utf-8'))
        print (Arduino_sensor_data)
        outF.close()
        outF=open("HAB3RadioData.txt",'a')
        outF.write(LOCtimeSTR+' '+str(Arduino_sensor_data)+ GPS_Sensor_data +'\n')
        sleep(1)

# create two new threads
ardunio_thread = Thread(target=arduino_sensors)
pi_thread = Thread(target=pi_sensors)
transmit_thread = Thread(target=transmit_data)

# start the threads
ardunio_thread.start()
pi_thread.start()
transmit_thread.start()
