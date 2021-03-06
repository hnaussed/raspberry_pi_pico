from machine import I2C, Pin
from sh1106 import SH1106_I2C
from time import sleep
import framebuf

WIDTH  = 128                                           # oled display width
HEIGHT = 64                                            # oled display height

sda = Pin(4)
scl = Pin(5)

i2c = I2C(0, sda=sda, scl=scl )  

devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))


oled = SH1106_I2C(WIDTH, HEIGHT, i2c) 

# Raspberry Pi logo as 32x32 bytearray
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

while True:
  oled.fill(0)
  oled.show()
  sleep(2)

  for loop_var in range(6):
    oled.text("Hallo"+str(loop_var),1+6*loop_var,1+8*loop_var)
    oled.show()
    sleep(2)
    
  oled.blit(fb, 96, 0)
  oled.show()
  sleep(2)



