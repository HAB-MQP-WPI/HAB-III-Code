import csv
import requests
import matplotlib.pyplot as plt
import numpy as np

time = [0]
CO2 = [0]
Pressure = [0]
Temp = [0]
Alt = [0]
OZ = [0]
UV = [0]
NO = [0]
PP = [0]
PT = [0]
LAT = [0]
LON = [0]
ALT = [0]
zero_list = []

x = open("Basedata.txt", "r")


while 1:
    line = x.readline()
    if str(line[0:12]) == "b\'03/13/2022":
        a = line.strip("b\'03/13/2022")
        a = a.replace('\\', '')
        b = a.strip(" n\n\'")
        time.append(b)
    if str(line[0:7]) == "b\"b\'P: ":
        a = line.strip("b\"b\'P: ")
        b = a.strip(" hPa\\r\\n'\n\"")
        Pressure.append(float(b))
        if len(Pressure) != len(time):
            Pressure.insert(-2, Pressure[-2])
    if str(line[0:7]) == "b\"b\'T: ":
        a = line.strip("b\"b\'T: ")
        b = a.strip(" C\\r\\n'\n\"")
        Temp.append(float(b))
        if len(Temp) != len(time):
            Temp.insert(-2, Temp[-2])
    if str(line[0:7]) == "b\"b\'A: ":
        a = line.strip("b\"b\'A: ")
        b = a.strip(" m\\r\\n'\n\"")
        Alt.append(float(b))
        if len(Alt) != len(time):
            Alt.insert(-2, Alt[-2])
    if str(line[0:8]) == "b\"b\'OZ: ":
        a = line.strip("b\"b\'OZ: ")
        b = a.strip(" ppb\\r\\n'\n\"")
        OZ.append(int(b))
        if len(OZ) != len(time):
            OZ.insert(-2, OZ[-2])
    if str(line[0:8]) == "b\"b\'CO2:":
        a = line.strip("b\"b\'CO2:<")
        b = a.strip("ppm\\n'\n\"")
        CO2.append(int(b))
        if len(CO2) != len(time):
            CO2.insert(-2, CO2[-2])
    if str(line[0:8]) == "b\"b\'UV: ":
        a = line.strip("b\"b\'UV: ")
        b = a.strip("\\r\\n'\n\"")
        UV.append(float(b)/12.7)
        if len(UV) != len(time):
            UV.insert(-2, UV[-2])
    if str(line[0:8]) == "b\"b\'NO: ":
        a = line.strip("b\"b\'NO: ")
        b = a.strip(" ppb\\r\\n'\n\"")
        NO.append(float(b))
        if len(NO) != len(time):
            NO.insert(-2, NO[-2])
    # Not Necssary for Plotting
    if str(line[0:6]) == "b\'PT: ":
        a = line.strip("b\'PT: ")
        a = a.replace('\\','')
        b = a.strip(" Cn\n\'")
        PT.append(float(b))
        if len(PT) != len(time):
            PT.insert(-2, PT[-2])
    if str(line[0:5]) == "b\'PP:":
        a = line.strip("b\'PP: ")
        a = a.replace('\\', '')
        b = a.strip(" mBarn\n\'")
        PP.append(float(b))
        if len(PP) != len(time):
            PP.insert(-2, PP[-2])
    if str(line[0:6]) == "b\'LAT:":
        a = line.strip("b\'LAT:  ")
        a = a.replace('\\', '')
        b = a.strip(" n\n\'")
        LAT.append(float(b))
        if float(b) == 0:
            zero_list.append(len(LAT))
        if len(LAT) != len(time):
            LAT.insert(-2, LAT[-2])
    if str(line[0:6]) == "b\'LON:":
        a = line.strip("b\'LON: ")
        a = a.replace('\\', '')
        b = a.strip(" n\n\'")
        LON.append(float(b))
        if len(LON) != len(time):
            LON.insert(-2, LON[-2])
    if str(line[0:6]) == "b\'ALT:":
        a = line.strip("b\'ALT: ")
        a = a.replace('\\', '')
        b = a.strip(" mn\n\'")
        ALT.append(float(b))
        if len(ALT) != len(time):
            ALT.insert(-2, ALT[-2])
    if line == '':
        break

    # url = 'https://api.thingspeak.com/update.json?api_key=NH6FE4DG7WM873WT&field1='+str(Pressure[-1])+'&field2='+str(Temp[-1])+'&field3='+str(Alt[-1])+'&field4='+str(OZ[-1])+'&field5='+str(CO2[-1])+'&field6='+str(UV[-1])+'&field7='+str(NO[-1])
    # y = requests.post(url)
    # if y.text != '0':
    #     print(y.text)

# data_out = open("Data_Out.txt", "w")
# data_out.write("Time \n")
# data_out.write(str(time))
# data_out.write("\nCO2 \n")
# data_out.write(str(CO2))
# data_out.write("\nPressure \n")
# data_out.write(str(Pressure))
# data_out.write("\nTemperature Sensor \n")
# data_out.write(str(Temp))
# data_out.write("\nAlt Sensor \n")
# data_out.write(str(Alt))
# data_out.write("\nOzone \n")
# data_out.write(str(OZ))
# data_out.write("\nUV \n")
# data_out.write(str(UV))
# data_out.write("\nPi Pressure \n")
# data_out.write(str(PP))
# data_out.write("\nPi Temperature \n")
# data_out.write(str(PT))
# data_out.write("\nLatitude \n")
# data_out.write(str(LAT))
# data_out.write("\nLongitude \n")
# data_out.write(str(LON))
# data_out.write("\nPi Altitude \n")
# data_out.write(str(ALT))

data_out = open("Data_out.csv","w",encoding='UTF-8')
writer = csv.writer(data_out)
writer.writerow("Time \n")
writer.writerow(time)
writer.writerow("\nCO2 \n")
writer.writerow(CO2)
writer.writerow("\nPressure \n")
writer.writerow(Pressure)
writer.writerow("\nTemperature Sensor \n")
writer.writerow(Temp)
writer.writerow("\nAlt Sensor \n")
writer.writerow(Alt)
writer.writerow("\nOzone \n")
writer.writerow(OZ)
writer.writerow("\nUV \n")
writer.writerow(UV)
writer.writerow("\nPi Pressure \n")
writer.writerow(PP)
writer.writerow("\nPi Temperature \n")
writer.writerow(PT)
writer.writerow("\nLatitude \n")
writer.writerow(LAT)
writer.writerow("\nLongitude \n")
writer.writerow(LON)
writer.writerow("\nPi Altitude \n")
writer.writerow(ALT)

time_index = np.arange(len(time))

plt.figure(1)
plt.plot(time_index[1::], Pressure[1::])
plt.xlabel("Time in Seconds")
plt.ylabel("Pressure in hPa")
plt.title("Pressure Sensor Data")

plt.figure(2)
plt.plot(time_index[1::], Temp[1::])
plt.xlabel("Time in Seconds")
plt.ylabel("Temperature in C")
plt.title("Temperature Sensor Data")

plt.figure(3)
plt.plot(time_index[1::], Alt[1::])
plt.xlabel("Time in Seconds")
plt.ylabel("Altitude in m")
plt.title("Altitude Sensor Data")

plt.figure(4)
plt.plot(time_index[1::], CO2[1::])
plt.xlabel("Time in Seconds")
plt.ylabel("CO2 in ppm")
plt.title("CO2 Sensor Data")

plt.figure(5)
plt.plot(time_index[1::], OZ[1::])
plt.xlabel("Time in Seconds")
plt.ylabel("Ozone in ppb")
plt.title("Ozone Sensor Data")

plt.figure(6)
plt.plot(time_index[1::], UV[1::])
plt.xlabel("Time in Seconds")
plt.ylabel("UV index")
plt.title("UV Sensor Data")

plt.figure(7)
plt.plot(time_index[1::], PP[1::])
plt.xlabel("Time in Seconds")
plt.ylabel("Pressure in mBar")
plt.title("Pi Internal Pressure Sensor Data")

plt.figure(8)
plt.plot(time_index[1::], PT[1::])
plt.xlabel("Time in Seconds")
plt.ylabel("Temperature in C")
plt.title("Pi Internal Temperature Sensor Data")


for i in range(len(zero_list)+1):
    LAT.remove(0)
    LON.remove(0)
    ALT.remove(0)
gps_time = np.arange(len(LAT))

plt.figure(9)
plt.plot(gps_time, LAT)
plt.xlabel("Time in Seconds")
plt.ylabel("Latitude in Decimal")
plt.title("GPS LAT Sensor Data")

plt.figure(10)
plt.plot(gps_time, LON)
plt.xlabel("Time in Seconds")
plt.ylabel("Longitude in Decimal")
plt.title("GPS LONG Sensor Data")

plt.figure(11)
plt.plot(gps_time, ALT)
plt.xlabel("Time in Seconds")
plt.ylabel("Altitude in m")
plt.title("GPS Altitude Data")

plt.figure(12)
plt.plot(LAT, LON)
plt.xlabel("Latitude in Decimal")
plt.ylabel("Longitude in Decimal")
plt.title("GPS Coordinate Data")

plt.show()
