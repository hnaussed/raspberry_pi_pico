
import machine
import time
import mqtt_config

from connect_2_wlan import connect_to_network,wlan
from umqtt_simple import MQTTClient

mqttBroker = '192.168.178.55'
mqttClient = 'pico'
mqttUser = mqtt_config.user
mqttPW = mqtt_config.password
mqttTopic = b"sensors/temperature/bedroom"

led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
sensor_temp = machine.ADC(4)

def getTemp():
    read = sensor_temp.read_u16()
    spannung = read * 3.3 / (65535)
    temperatur = 27 - (spannung - 0.706) / 0.001721
    return temperatur

connect_to_network()

if wlan.isconnected():
    print('WLAN-Verbindung hergestellt / WLAN-Status:', wlan.status())
    print()
    led_onboard.on()
else:
    print('Keine WLAN-Verbindung / WLAN-Status:', wlan.status())
    print()
    led_onboard.off()

# Funktion: Verbindung zum MQTT-Server herstellen
def mqttConnect():
    if mqttUser != '' and mqttPW != '':
        print("MQTT-Verbindung herstellen: %s mit %s als %s" % (mqttClient, mqttBroker, mqttUser))
        client = MQTTClient(mqttClient, mqttBroker, user=mqttUser, password=mqttPW, keepalive=60)
    else:
        print("MQTT-Verbindung herstellen: %s mit %s" % (mqttClient, mqttBroker))
        client = MQTTClient(mqttClient, mqttBroker, keepalive=60)
    client.connect()
    print()
    print('MQTT-Verbindung hergestellt')
    print()
    return client

# Funktion zur Taster-Auswertung
while True:
    myValue = str(getTemp())
    try:
        client = mqttConnect()
        client.publish(mqttTopic, myValue)
        print("An Topic %s gesendet: %s" %  (mqttTopic, myValue))
        print()
        client.disconnect()
        print('MQTT-Verbindung beendet')
        print()
    except OSError:
        print()
        print('Fehler: Keine MQTT-Verbindung')
        print()
    # 60 Sekunden warten
    time.sleep(60)