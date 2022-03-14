 #!/usr/bin/env python
import time
import serial

ser1 = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

ser2=serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

outF=open("HAB3SensorData.txt","w")
outF.write('Start of Arduino Sensor Data\n')
#outF.close()
#outF=open("HAB3SensorData.txt",'a')

while 1:
        x=ser1.readline()
        ser2.write(bytes((str(x)+ '\n'), 'utf-8'))
        outF.close()
        outF=open("HAB3SensorData.txt",'a')
        outF.write(str(x)+'\n')
        print (x)
