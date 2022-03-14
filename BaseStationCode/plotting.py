import requests

CO2 = [0]
Pressure = [0]
Temp = [0]
Alt = [0]
OZ = [0]
UV = [0]
NO = [0]
x = open("Basedata.txt", "r")


while 1:
    line = x.readline()
    if str(line[0:7]) == "b\"b\'P: ":
        a = line.strip("b\"b\'P: ")
        b = a.strip(" hPa\\r\\n'\n\"")
        Pressure.append(float(b))
    if str(line[0:7]) == "b\"b\'T: ":
        a = line.strip("b\"b\'T: ")
        b = a.strip(" C\\r\\n'\n\"")
        Temp.append(float(b))
    if str(line[0:7]) == "b\"b\'A: ":
        a = line.strip("b\"b\'A: ")
        b = a.strip(" m\\r\\n'\n\"")
        Alt.append(float(b))
    if str(line[0:8]) == "b\"b\'OZ: ":
        a = line.strip("b\"b\'OZ: ")
        b = a.strip(" ppb\\r\\n'\n\"")
        OZ.append(int(b))
    if str(line[0:8]) == "b\"b\'CO2:":
        a = line.strip("b\"b\'CO2:")
        b = a.strip("ppm\\n'\n\"")
        CO2.append(int(b))
    if str(line[0:8]) == "b\"b\'UV: ":
        a = line.strip("b\"b\'UV: ")
        b = a.strip("\\r\\n'\n\"")
        UV.append(float(b))
    if str(line[0:8]) == "b\"b\'NO: ":
        a = line.strip("b\"b\'NO: ")
        b = a.strip(" ppb\\r\\n'\n\"")
        NO.append(float(b))

    url = 'https://api.thingspeak.com/update.json?api_key=NH6FE4DG7WM873WT&field1='+str(Pressure[-1])+'&field2='+str(Temp[-1])+'&field3='+str(Alt[-1])+'&field4='+str(OZ[-1])+'&field5='+str(CO2[-1])+'&field6='+str(UV[-1])+'&field7='+str(NO[-1])
    y = requests.post(url)
    if y.text != '0':
        print(y.text)
