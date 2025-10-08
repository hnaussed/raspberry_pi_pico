import usocket as socket
import ustruct as struct
import urequests
import time
import machine
import wlan_config
import rp2

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

def setPCFTime( pcf ):
    ntpTime = getNTPTime()
    timezone = getTZInfo()

    if timezone["isDayLightSavingActive"]:
        tm = time.gmtime(ntpTime + timezone["standardUtcOffset"]["seconds"] + timezone["dstInterval"]["dstOffsetToStandardTime"]["seconds"])
    else:
        tm = time.gmtime(ntpTime + timezone["standardUtcOffset"]["seconds"] )

    pcf.set_datetime(( tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5]))

def syncRTCTime( pcf ):
    # (year, month, date, day, hours, minutes, seconds
    (year, month, day, weekday, hours, minutes, seconds ) = pcf.datetime()
    #(year, month, day, weekday, hours, minutes, seconds, subseconds)
    machine.RTC().datetime(( 2000+year, month, day, weekday, hours, minutes, seconds,0))

def wlanConnect( wlan ):

    rp2.country("DE")
    led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
 

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

def wlanDisconnect( wlan ):
    # WLAN ordnungsgemäß beenden
    wlan.disconnect()
    wlan.active(False)
    wlan.deinit()
    time.sleep_ms(100)

