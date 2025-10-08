# Gemeinsame MQTT-Hilfsfunktionen für Pico W Beispiele
# Erwartet: mqtt_config.py mit Variablen user, password (optional leer)
# Nutzung:
#   from mqtt_common import mqtt_connect
#   client = mqtt_connect(client_id, broker, keepalive=60)
#   client.publish(topic, payload)
#   client.disconnect()

from umqtt_simple import MQTTClient
import mqtt_config


def mqtt_connect(client_id: str, broker: str, keepalive: int = 60):
    """Stellt eine MQTT-Verbindung her und gibt den Client zurück.

    Wählt automatisch Authentifizierung, falls user/password gesetzt.
    """
    user = getattr(mqtt_config, 'user', '')
    password = getattr(mqtt_config, 'password', '')
    if user and password:
        print("MQTT: Verbinden als %s zu %s" % (client_id, broker))
        client = MQTTClient(client_id, broker, user=user, password=password, keepalive=keepalive)
    else:
        print("MQTT: Verbinden als %s zu %s (ohne Auth)" % (client_id, broker))
        client = MQTTClient(client_id, broker, keepalive=keepalive)
    client.connect()
    print("MQTT: Verbunden")
    return client
