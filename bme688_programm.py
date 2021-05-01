from machine import I2C, Pin
from bme680 import *
from time import sleep

sda = machine.Pin(26) 
scl = machine.Pin(27)
i2c = machine.I2C(1,sda=sda,scl=scl,freq=400000) 

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))
 
  for device in devices:  
     #hex( device ) gives me this error ( TypeError: object with buffer protocol required )
    print("Device: ",str(device))

bme = BME680_I2C( i2c)

while True: 
    print("Temp:", bme.temperature, "Feuchtigkeit:", bme.humidity, "Druck:", bme.pressure, "Gas:", bme.gas)
    sleep(10)