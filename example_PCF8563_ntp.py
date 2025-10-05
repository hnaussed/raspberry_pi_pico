import module_common
import machine
import network
import pcf8563


# Initialisierung I2C
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

# I2C-Bus-Scan ausgeben
print(i2c.scan())

pcf = pcf8563.PCF8563( i2c )
wlan = network.WLAN(network.STA_IF)

# WLAN-Verbindung herstellen
module_common.wlanConnect( wlan )

# Zeit setzen
module_common.setPCFTime( pcf )
module_common.syncRTCTime( pcf )

module_common.wlanDisconnect( wlan)

while True:
    
    module_common.syncRTCTime( pcf )
    print("-" * 20)
    print(machine.RTC().datetime())
    print(pcf.datetime())
    machine.lightsleep(5000)

