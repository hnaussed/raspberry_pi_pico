import machine
import time

led = machine.Pin(15, machine.Pin.OUT)
sensor = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    if sensor.value() == 0:
        led.value(1)
        time.sleep(1)
    led.value(0)