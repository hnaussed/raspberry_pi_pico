import bme680 
import sh1106
import machine
import pcf8563
import time
import network
import module_common
import mqtt_config  # erwartet Variablen user, password
from mqtt_common import mqtt_connect

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

display = sh1106.SH1106_I2C( width=128, height=64, i2c=i2c, rotate=180)
bme = bme680.BME680_I2C(i2c)
pcf = pcf8563.PCF8563( i2c )
wlan = network.WLAN(network.STA_IF)

# MQTT Konfiguration
mqttBroker = '192.168.178.55'  # ggf. anpassen
mqttClient = 'pico-bme680'
mqttUser = mqtt_config.user
mqttPW = mqtt_config.password
# Mehrere Topics (Bytes) für strukturierte Daten
mqttTopicTemp = b"sensors/bme680/temperature"
mqttTopicHum = b"sensors/bme680/humidity"
mqttTopicPres = b"sensors/bme680/pressure"
mqttTopicGas = b"sensors/bme680/gas"
mqttTopicAlt = b"sensors/bme680/altitude"



module_common.wlanConnect( wlan )
module_common.setPCFTime( pcf )
module_common.syncRTCTime( pcf )
# WLAN wieder trennen um Energie zu sparen; wird für MQTT erneut aufgebaut
module_common.wlanDisconnect( wlan)

# Publish-Intervall in Sekunden
PUBLISH_INTERVAL = 60
last_publish = time.time() - PUBLISH_INTERVAL  # sofort beim Start senden
client = None  # wird lazy erstellt

while True:
    # Messwerte lesen (einmal je Loop für Konsistenz)
    temp = bme.temperature
    hum = bme.humidity
    pres = bme.pressure
    gas = bme.gas
    alt = bme.altitude

    display.fill(0)
    display.text(f" Temp: {temp:0.1f} C", 0, 0, 1)
    display.text(f"  Hum: {hum:0.1f} %%", 0, 10, 1)
    display.text(f"Press: {pres:0.3f} HPa", 0, 20, 1)
    display.text(f"  Gas: {gas:d} ohm", 0, 30, 1)
    display.text(f"  Alt: {alt:0.2f} m", 0, 40, 1)
    rtctime = machine.RTC().datetime()
    pcftime = pcf.datetime()
    # Debug-Ausgabe optional
    # print(rtctime)
    # print(pcftime)
    display.text(f"{pcftime[0]:02d}.{pcftime[1]:02d}.{pcftime[2]:02d} {pcftime[4]:02d}:{pcftime[5]:02d}:{pcftime[6]:02d}",0,50,1 )
    display.show()

    # Periodisch MQTT publish
    now = time.time()
    if now - last_publish >= PUBLISH_INTERVAL:
        try:
            # WLAN verbinden falls getrennt
            if not wlan.isconnected():
                module_common.wlanConnect( wlan )
            if client is None:
                client = mqtt_connect(mqttClient, mqttBroker, keepalive=60)
            # Einzelne Werte senden
            client.publish(mqttTopicTemp, f"{temp:0.2f}")
            client.publish(mqttTopicHum, f"{hum:0.2f}")
            client.publish(mqttTopicPres, f"{pres:0.2f}")
            client.publish(mqttTopicGas, str(gas))
            client.publish(mqttTopicAlt, f"{alt:0.2f}")
            print("MQTT: Messwerte gesendet")
            last_publish = now
            # Verbindung bewusst kurz halten: trennen um Energie/WLAN Last zu sparen
            client.disconnect()
            client = None
            module_common.wlanDisconnect( wlan )
        except Exception as e:
            print("MQTT Fehler:", e)
            # Fehlerfall: sauber versuchen zu schließen
            try:
                if client:
                    client.disconnect()
            except:
                pass
            client = None
            # WLAN ggf. zurücksetzen
            if wlan.isconnected():
                module_common.wlanDisconnect( wlan )
            # nächster Versuch im nächsten Intervall
            last_publish = now  # verhindert sofortiges Retriggern

    time.sleep(1)
