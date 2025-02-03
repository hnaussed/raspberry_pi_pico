from machine import Pin
import time
led_external_1 = Pin(15, Pin.OUT)
led_external_2 = Pin(13, Pin.OUT)
button = Pin(14, Pin.IN)

while True:
   if button.value() == 1:
      led_external_1.value(1)
      led_external_2.value(0)
      time.sleep(2)
   led_external_1.value(0)
   led_external_2.value(1)