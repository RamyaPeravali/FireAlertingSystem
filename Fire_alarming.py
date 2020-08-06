#pip install ibmiotf (for ibm platform)
#git clone https://github.com/szazo/DHT11_python.git (dht11 library)

import RPi.GPIO as GPIO
import dht11
import time
import sys
import ibmiotf.application
import imbiotf.device
from os.path import join,dirname
from os import environ
from pprint import pprint

#IBM Watson Device Credentials
organization = "5zb68x"
deviceType= "raspberry"
deviceId = "srs"
authMethod ="token"
authTokeen = "J2udMgam3LRNen)fyD"
#Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(16,GPIO.OUT)
GPIO.setup(21,GPIO.IN)

SensorInstance = dht11.DHT11(pin=21)
adc = MCP3208()
#while True:
    #SensorInstance1 = adc.read(0)
    #print('adc[0]', SensorInstance1)
#Initialize the device client.
try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli = ibmiotf.device.Client(deviceOptions) #connect to ibmm iot platform
except Exception as e:
    print("Caught exception connecting device: %s" % str(e))
    sys.exit() #terminate program

def mycommandCallback(cmd):
    print("command received: %s" % cmd.data['command'])
    s=str(cmd.data['command'])
    print(s)
    if(s=="LIGHTON"):
        GPIO.output(16,True)
    elif(s=="LIGHTOFF"):
        GPIO.output(16,False)

deviceCli.connect()
while True:
    SensorData=SensorInstance.read()
    SensorInstance1=adc.read(0)

    if SensorDats.is_valid():
        T = SensorData.temperature
        H = SensorData.humidity
        data={'Temperature' : T,'Humidity' : H}
        def myOnpublishCallback():
            print ("Published Temperature = %s C" %T,"Humidity = %s %%" %H, "to IBM Watson")
        success = deviceCli.publishEvent("DHT11","json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
    else:
        print ("SensorData Invalid")
    if  SensorInstance1.is_valid():
        S = SensorInstance1.smoke()
        #H = SensorData.humidity
        data1 = {'Smoke' : S}
        def myOnPublicCallback():
            print("Published Smoke = %s " %S, "to IBM Watson")
        success = deviceCli.publishEvent("MCP3208","json",data1,qos=0,on_publish=myOnPublishCallback) 
        if not success:
            print("Not Connected to ToTF")
        time.sleep(2)
    else:
        print("SensorData Invalid")
    deviceCli.commandCallbackk=mycommandCallback

#Disconnect the device and application from the cloud
deviceCli.disconnect()
