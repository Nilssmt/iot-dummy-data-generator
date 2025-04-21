import time
import paho.mqtt.client as paho
from paho import mqtt
import web3_connection

path_to_save = "PATH"




# Callback, wenn die Verbindung erfolgreich ist
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    client.subscribe("iot/sensor/data/temperature", qos=1)
    client.subscribe("iot/sensor/data/humidity", qos=1)
    client.subscribe("iot/sensor/data/light", qos=1)
    client.subscribe("iot/sensor/data/movement", qos=1)
    client.subscribe("iot/sensor/data/co2", qos=1)

# Callback, wenn eine Nachricht empfangen wurde
def on_message(client, userdata, msg):
    data = msg.payload.decode()  # Direkt als String speichern
    print(f"Received message from {msg.topic}: {data}")
    save_data_to_file(data)
    web3_connection.send_data_to_contract(data)


def save_data_to_file(data):
    with open(path_to_save, "a") as file:
        file.write(data + "\n")

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

# TLS aktivieren (sichere Verbindung)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

client.username_pw_set("NAME", "PASSOWRD")

client.connect("URL", 8883)

client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnected from MQTT broker.")
    client.loop_stop()
