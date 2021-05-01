from machine import I2C, Pin
from bme680 import BME680_I2C
from sh1106 import SH1106_I2C
from time import sleep

WIDTH  = 128                                           # oled display width
HEIGHT = 64                                            # oled display height

sda = Pin(26) 
scl = Pin(27)
i2c = I2C(1,sda=sda,scl=scl,freq=400000) 

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))
 
  for device in devices:  
     #hex( device ) gives me this error ( TypeError: object with buffer protocol required )
    print("Device: ",str(device))

bme = BME680_I2C( i2c )
oled = SH1106_I2C(WIDTH, HEIGHT, i2c) 



while True: 
    oled.fill(0)
    oled.show()

    temperature      = "{:^7.2f}".format(bme.temperature ) + " C"
    luftfeuchtigkeit = "{:^7.2f}".format(bme.humidity  )   + " %"
    druck            = "{:^7.2f}".format(bme.pressure )    + " hPa"
    gas              = "{:^7.1f}".format(bme.gas/1000 )    + " KOms"

    print("Temp: ", temperature, "Feuchtigkeit: ", luftfeuchtigkeit, "Druck: ", druck, "Gas: ", gas)

    oled.text("Tem:"+temperature,1,1 )
    oled.text("Hum:"+luftfeuchtigkeit,1,1+8 )
    oled.text("Pre:"+druck, 1, 1+16 )
    oled.text("Gas:"+gas, 1, 1+24 )
    oled.show()
    sleep(10)

    