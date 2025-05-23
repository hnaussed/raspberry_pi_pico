import bme680 
import ssd1306
import machine
import time

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

# I2C-Bus-Scan
print('Scan I2C Bus...')
devices = i2c.scan()

# Scanergebnis ausgeben
if len(devices) == 0:
    print('Kein I2C-Gerät gefunden!')
else:
    print('I2C-Geräte gefunden:', len(devices))
    for device in devices:
        print('Dezimale Adresse:', device, '| Hexadezimale Adresse:', hex(device))

display = ssd1306.SSD1306_I2C(128, 32, i2c)
 
display.text("Hello, Pico!", 0, 0, 1)
display.show()

bme = bme680.BME680_I2C(i2c)

while True:
#    print(bme.temperature, bme.humidity, bme.pressure, bme.gas)
    display.fill(0)
    display.text(f"Temp:  {bme.temperature}", 0, 0, 1)
    display.text(f"Hum:   {bme.humidity}", 0, 10, 1)
    display.text(f"Press: {bme.pressure}", 0, 20, 1)
    display.text(f"Gas:   {bme.gas}", 0, 30, 1)
    display.show()
    time.sleep(1)
