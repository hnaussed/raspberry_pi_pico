
import machine
import time
import mqtt_config
import bme680 



from connect_to_wlan import connect_to_wlan
from umqtt_simple import MQTTClient

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
        
bme = bme680.BME680_I2C(i2c)

led_onboard = machine.Pin('LED', machine.Pin.OUT, value=0)
sensor_temp = machine.ADC(4)

def getPicoTemp():
    read = sensor_temp.read_u16()
    spannung = read * 3.3 / (65535)
    temperatur = 27 - (spannung - 0.706) / 0.001721
    return temperatur

wlan = connect_to_wlan()

if wlan.isconnected():
    print('WLAN-Verbindung hergestellt / WLAN-Status:', wlan.status())
    print()
    led_onboard.on()
else:
    print('Keine WLAN-Verbindung / WLAN-Status:', wlan.status())
    print()
    led_onboard.off()

# Funktion: Verbindung zum MQTT-Server herstellen

mqttBroker = '192.168.178.55'
mqttClient = 'pico'
mqttUser   = mqtt_config.user
mqttPW     = mqtt_config.password

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

       
    try:
        messages = { 
                'iot/pico/temp': str(round(getPicoTemp(),2) ),
                'iot/pico/bme/temp':  str( round( bme.temperature, 2 ) ),
                'iot/pico/bme/hum': str ( round( bme.humidity, 2 ) ),
                'iot/pico/bme/pres':  str ( round( bme.pressure, 2 ) ),
                'iot/pico/bme/gas': str ( round( bme.gas/1000, 2 ) ) }
        
        client = mqttConnect()
        
        for message in messages:
            client.publish( message, messages[message] )
            print("Topic %s gesendet: %s" %  ( message, messages[message] ))   
             
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