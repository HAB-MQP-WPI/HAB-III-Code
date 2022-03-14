#https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/
#python -m pip install -- upgrade pynmeagps

import os
import glob
import ms5803py
import serial
import time
import pynmeagps
from gpiozero import CPUTemperature

stream = serial.Serial('/dev/ttyUSB1',9600)
nmr = pynmeagps.NMEAReader(stream)
cpu = CPUTemperature()
s = ms5803py.MS5803()
GPStime = ''
GPSlat = 0
GPSlong = 0
GPSalt = 0
GPSsats = 0
wTemp = 0
pTemp = 0
pPres = 0

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

GPS_F=open("HAB3GPSData.txt","w")
GPS_F.write('Start of GPS Data\n')

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

while True:
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
    
    print("\nCPUtemp {:4.2f} wTemp {:4.2f} pTemp {:4.2f} pPres {} Time {} UTC {} Lat {:10.8f} Long {:10.8f} Altitude {:8.1f} #Sats {:2d}".format(CPUTemp,wTemp, pTemp,pPres,LOCtimeSTR,GPStime,GPSlat, GPSlong,GPSalt,GPSsats))
