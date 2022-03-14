import serial
from serial.tools import list_ports
import numpy as np
import matplotlib.pyplot as plt

list1 = list_ports.comports()
connected = []
for element in list1:
    connected.append(element.device)
print("Connected COM ports: " + str(connected))

ser = serial.Serial(
        port='COM3',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
ser.close()
ser.open()
outF = open("Basedata.txt", "a")
outF.write('Start of Sensor Data\n')
print(ser.isOpen())

while 1:
    x = ser.readline()
    outF = open("Basedata.txt", "a")
    outF.write(str(x))
    outF.write('\n')
    print(str(x))
