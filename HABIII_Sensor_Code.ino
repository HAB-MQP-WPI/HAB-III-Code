      /*
 * HAB III Sensor Code:
 *    This is the code for the Ardunio Uno onboard the payload. It is designed to 
 *    take inputs from the BMP(barametric preasure sensor), UV, CO2, Ozone and 
 *    internal temperature sensor. This sensor data is then transmitted the the 
 *    Pi where it is stored and transmitted via antenna. 
 *      Date        Modifications   Author
 *      11/1/2021   Created         Madeline Kasznay
 */

//Libraries
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include "DFRobot_OzoneSensor.h"

//Sensor Pins
#define CO2_PIN (A3)
#define UV_PIN (A0)
#define NO_PIN (A2)


//Constants
float NO2resistance; //NO2 variables
float NO2SeriesResistor = 2200;
#define ADC_OFFSET 0
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);
#define COLLECT_NUMBER   20 // collect number for the ozone sensor, the collection range is 1-100
#define Ozone_IICAddress ADDRESS_3
DFRobot_OzoneSensor Ozone;
#define BOOL_PIN (2)
#define DC_GAIN (8.5) //define the DC gain of amplifier
#define READ_SAMPLE_INTERVAL (50) //CO2 sample amount
#define READ_SAMPLE_TIMES (5) //define the time interval(in milisecond) between each samples

//These two values differ from sensor to sensor. user should derermine this value.
#define ZERO_POINT_VOLTAGE           (0.220) //define the output of the sensor in volts when the concentration of CO2 is 400PPM
#define REACTION_VOLTGAE             (0.030) //define the voltage drop of the sensor when move the sensor from air into 1000ppm CO2

float CO2Curve[3] = {2.602,ZERO_POINT_VOLTAGE,(REACTION_VOLTGAE/(2.602-3))};

// The setup loop which intializes all of the sensors
void setup() {
  
Serial.begin(9600);

// Intialize the BMP sensor
if(!bmp.begin()){
  Serial.print("Ooops, no BMP085 detected ... Check your wiring or I2C ADDR!");
  while(1);
}
// Intialize the Ozone Sensor
 
while(!Ozone.begin(Ozone_IICAddress)) {
  Serial.println("I2c Ozone device number error !");
  delay(1000);
}  Serial.println("I2c Ozone connect success !");
Ozone.SetModes(MEASURE_MODE_PASSIVE);

// Intialize the CO2 Sensor
    pinMode(BOOL_PIN, INPUT);                        //set pin to input
    digitalWrite(BOOL_PIN, HIGH);                    //turn on pullup resistors
    
}

void loop() {

//Start to read sensor values
//Serial.println("\nStart to read Sensor values:");

//Read the BMP Sensor Values
    sensors_event_t event;
    bmp.getEvent(&event);
    if (event.pressure){
      Serial.print("P: "); Serial.print(event.pressure); Serial.println(" hPa");
      float temperature; bmp.getTemperature(&temperature);
      Serial.print("T: "); Serial.print(temperature); Serial.println(" C");
      float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;
      Serial.print("A: "); Serial.print(bmp.pressureToAltitude(seaLevelPressure,event.pressure,temperature)); Serial.println(" m");
    }
    else{
      Serial.println("BMP Sensor error");
    } 

//Read the Ozone Sensor Values
int16_t ozoneConcentration = Ozone.ReadOzoneData(COLLECT_NUMBER);
Serial.print("OZ: "); Serial.print(ozoneConcentration); Serial.println(" ppb");

//Read the CO2 sensor values
    int percentage;
    float volts;
    volts = MGRead(CO2_PIN);
    percentage = MGGetPercentage(volts,CO2Curve);
    Serial.print("CO2:");
    if (percentage == -1) {
        Serial.print( "<400" );
    } else {
        Serial.print(percentage);
    }
    Serial.print( " ppm" );
    Serial.print("\n");
                                

//Read the UV sensor values 
  float sensorValue;
  sensorValue = analogRead(UV_PIN);
  Serial.print("UV: ");
  Serial.print(sensorValue);
  Serial.println("");

/*
//Read the NO sensor voltage
  int NO2Reading = analogRead(NO_PIN) + 1; // Get raw sensor reading for UV Sensor
  float NO2Resistance = NO2SeriesResistor * ((1023.0 / (NO2Reading - ADC_OFFSET)) -1); //Convert reading into resistance value
  float NO2_index = NO2Resistance / 100; //Convert into index
  Serial.print("NO: ");
  Serial.print((NO2_index/0.0409)/46.0055);
  Serial.println(" ppb");
  */

  delay(5000);
  
}

float MGRead(int mg_pin)
{
    int i;
    float v=0;

    for (i=0;i<READ_SAMPLE_TIMES;i++) {
        v += analogRead(mg_pin);
        delay(READ_SAMPLE_INTERVAL);
    }
    v = (v/READ_SAMPLE_TIMES) *5/1024 ;
    return v;
}

int  MGGetPercentage(float volts, float *pcurve)
{
   if ((volts/DC_GAIN )>=ZERO_POINT_VOLTAGE) {
      return -1;
   } else {
      return pow(10, ((volts/DC_GAIN)-pcurve[1])/pcurve[2]+pcurve[0]);
   }
}

int convertUV (float UVvalue) {
  int index;
  if (UVvalue < 50) {
    index = 0;
  }
  else if (UVvalue < 227) {
    index = 1;
  }
  else if (UVvalue < 318) {
    index = 2;
  }
  else if (UVvalue < 408) {
    index = 3;
  }
  else if (UVvalue < 503) {
    index = 4;
  }
  else if (UVvalue < 606) {
    index = 5;
  }
  else if (UVvalue < 696) {
    index = 6;
  }
  else if (UVvalue < 795) {
    index = 7;
  }
  else if (UVvalue < 881) {
    index = 8;
  }
  else if (UVvalue < 976) {
    index = 9;
  }
  else if (UVvalue < 1079) {
    index = 10;
  }
  else {
    index = 11;
  }
  return index;
}
