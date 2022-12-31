from machine import Pin
import time
led_external = Pin(15, Pin.OUT)
button = Pin(14, Pin.IN)

while True:
 if button.value() == 1:
    led_external.value(1)
    time.sleep(2)
 led_external.value(0)