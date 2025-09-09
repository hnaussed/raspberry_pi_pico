#https://github.com/lewisxhe/PCF8563_PythonLibrary/tree/master

import machine
import time

import network
import rp2

import pcf8563
import wlan_config

import usocket as socket
import ustruct as struct

import urequests

# Initialisierung I2C
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))

# I2C-Bus-Scan ausgeben
print(i2c.scan())

pcf = pcf8563.PCF8563( i2c )

def wlanConnect():

    rp2.country("DE")
    led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wlan_config.ssid, wlan_config.psk)
 
    max_wait = 30
    for i in range(max_wait):
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        led_onboard.toggle()
        print('.')
        time.sleep(1)
    if wlan.isconnected():
        print('WLAN-Verbindung hergestellt / WLAN-Status:', wlan.status())
        print(wlan.ifconfig())
        led_onboard.on()
    else:
        print('Keine WLAN-Verbindung')
        led_onboard.off()
        print('WLAN-Status:', wlan.status())
    
def getTZInfo():
    time_data_api = "https://www.timeapi.io/api/timezone/zone?timeZone=Europe%2FBerlin"
    try:
        res = urequests.get(time_data_api)
        tdata = res.json()
        return tdata
    except:
        raise Exception("Failed to query Time Data API")


def getNTPTime():
    NTP_HOST = 'pool.ntp.org'
    NTP_DELTA = 2208988800
    NTP_QUERY = bytearray(48)
    NTP_QUERY[0] = 0x1B
    addr = socket.getaddrinfo(NTP_HOST, 123)[0][-1]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.settimeout(1)
        res = s.sendto(NTP_QUERY, addr)
        msg = s.recv(48)
    finally:
        s.close()
    ntp_time = struct.unpack("!I", msg[40:44])[0]
    return ntp_time - NTP_DELTA

def setRTCTime():
    ntpTime = getNTPTime()
    timezone = getTZInfo()

    if timezone["isDayLightSavingActive"]:
        tm = time.gmtime(ntpTime + timezone["standardUtcOffset"]["seconds"] + timezone["dstInterval"]["dstOffsetToStandardTime"]["seconds"])
    else:
        tm = time.gmtime(ntpTime + timezone["standardUtcOffset"]["seconds"] )

    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], tm))
    pcf.write_all( tm[5], tm[4], tm[3], tm[6] + 1, tm[2], tm[1], tm[0] - 2000 )

# WLAN-Verbindung herstellen
wlanConnect()

# Zeit setzen
setRTCTime()

# Aktuelles Datum ausgeben
print()
print(machine.RTC().datetime())
print( pcf.datetime() )
