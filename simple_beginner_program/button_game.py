import machine
import time
import random

pressed = False
fastest_button = None

led = machine.Pin(15, machine.Pin.OUT)

right_button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)
left_button = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

def button_handler(pin):
    global pressed
    if not pressed:
        pressed=True
        print(pin)
        global fastest_button
        fastest_button = pin
        timer_reaction = time.ticks_diff(time.ticks_ms(), timer_start)
        print("Your reaction time was " + str(timer_reaction) +" milliseconds!")

led.value(1)
time.sleep(random.uniform(5, 10))
led.value(0)

timer_start = time.ticks_ms()

left_button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)
right_button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_handler)

while fastest_button is None:
    time.sleep(1)
if fastest_button is left_button:
    print("Left Player wins!")
elif fastest_button is right_button:
    print("Right Player wins!")