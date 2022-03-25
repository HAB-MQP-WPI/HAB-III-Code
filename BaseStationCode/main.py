import serial 
from serial.tools import list_ports
import numpy as np
import matplotlib.pyplot as plt

list1 = list_ports.comports() #lists active COM ports 
connected = []
for element in list1:
    connected.append(element.device) #Checks if COM port is connected
print("Connected COM ports: " + str(connected)) 

ser = serial.Serial(    #Sets up Serial Connection Parameters. Must be same as the radio's SPI settings
        port='COM3',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
ser.close() #closes the serial port if it was left open
ser.open()  #reopens the serial port
outF = open("Basedata.txt", "a") #Creates or opens Basedata.txt in appending mode as to not overwrite any preivous data
outF.write('Start of Sensor Data\n') #Writes header text to data file
print(ser.isOpen()) #Tells user in the serial port is open

while 1: #Constantly running
    x = ser.readline() #Reads data in from Serial port
    outF.write(str(x)) #Writes serial data to the text file
    outF.write('\n')   #Writes a new line to the data file
    print(str(x))      #Prints line to console so the user can see the activity
