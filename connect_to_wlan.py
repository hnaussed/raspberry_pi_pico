import time
import network
import rp2
import wlan_config

rp2.country("DE")
wlan = network.WLAN(network.STA_IF)
 
def connect_to_wlan():

    ssid = wlan_config.ssid
    psk = wlan_config.psk

    wlan.active(True)
    wlan.connect(ssid, psk)
    
    max_wait = 30
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print("Waiting for Wi-Fi connection...")
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError("Network connection failed")
    else:
        print("Connected to Wi-Fi network.")
        print(wlan.ifconfig())
    
    return wlan
        