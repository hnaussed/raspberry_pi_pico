from machine import Pin
import utime
 
red = Pin(16, Pin.OUT)
green = Pin(18, Pin.OUT)
blue = Pin(20, Pin.OUT)
 
red.value(0)
green.value(0)
blue.value(0)

while True:
    red.value(0)
    green.value(1)
    blue.value(1)
    print("rot")
    utime.sleep(3)
 
    red.value(1)
    green.value(0)
    blue.value(1)
    print("grün")
    utime.sleep(3)

    red.value(1)
    green.value(1)
    blue.value(0)
    print("blau")
    utime.sleep(3)