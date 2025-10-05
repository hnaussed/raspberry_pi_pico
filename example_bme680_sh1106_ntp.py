import bme680 
import sh1106
import machine
import pcf8563
import time
import network
import module_common

sda = machine.Pin(16)
scl = machine.Pin(17)
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

display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c,rotate=180)
bme = bme680.BME680_I2C(i2c)
pcf = pcf8563.PCF8563( i2c )
wlan = network.WLAN(network.STA_IF)


module_common.wlanConnect( wlan )
module_common.setPCFTime( pcf )
module_common.syncRTCTime( pcf )
module_common.wlanDisconnect( wlan)

while True:
#    print(bme.temperature, bme.humidity, bme.pressure, bme.gas)
    display.fill(0)
    display.text(f" Temp: {bme.temperature:.2f}", 0, 0, 1)
    display.text(f"  Hum: {bme.humidity:.2f}", 0, 10, 1)
    display.text(f"Press: {bme.pressure:.0f}", 0, 20, 1)
    display.text(f"  Gas: {bme.gas:.0f}", 0, 30, 1)
    rtctime = machine.RTC().datetime()
    pcftime = pcf.datetime()
    print(rtctime)
    print(pcftime)
    display.text(f"{rtctime[0]% 100:02d}.{rtctime[1]:02d}.{rtctime[2]:02d} {rtctime[4]:02d}:{rtctime[5]:02d}:{rtctime[6]:02d}",0,40,1)
    display.text(f"{pcftime[0]:02d}.{pcftime[1]:02d}.{pcftime[2]:02d} {pcftime[4]:02d}:{pcftime[5]:02d}:{pcftime[6]:02d}",0,50,1 )
    display.show()
    time.sleep(1)
