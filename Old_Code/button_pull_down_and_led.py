import machine
import utime

led_external = machine.Pin(15, machine.Pin.OUT)
button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

while True:
    if button.value() == 1:
        led_external.value(1)
        print("you pressed the button!")
    utime.sleep(2)
    led_external.value(0)