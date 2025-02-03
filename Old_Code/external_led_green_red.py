import machine
import utime

led_external_green = machine.Pin(15, machine.Pin.OUT)
led_external_red = machine.Pin(14, machine.Pin.OUT)

led_external_green.value(1)
led_external_red.value(0)

while True:
    led_external_green.toggle()
    led_external_red.toggle()
    utime.sleep(5)