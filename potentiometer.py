import machine
import utime

potentiometer = machine.ADC(26)

led = machine.PWM(machine.Pin(15))
led.freq(1000)

#conversion_factor = 3.3 / (65535)

while True:
    led.duty_u16(potentiometer.read_u16())

    #voltage = potentiometer.read_u16() * conversion_factor
    #print(voltage)
    #utime.sleep(2)