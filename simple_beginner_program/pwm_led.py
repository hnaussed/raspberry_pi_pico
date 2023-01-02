
from machine import Pin
from machine import PWM
from time import sleep

pwm = PWM(Pin(25, Pin.OUT))

pwm.freq(1000)

while True:
    for duty in range(65025):
        pwm.duty_u16(duty)
        sleep(0.0001)
    for duty in range(65025, 0, -1):
        pwm.duty_u16(duty)
        sleep(0.0001)
