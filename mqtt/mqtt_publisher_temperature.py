import time
import csv
import paho.mqtt.client as paho
from paho import mqtt

from time_interval import frequent_send_temperature

# Callback, wenn die Verbindung erfolgreich ist
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))

# Callback, wenn die Nachricht veröffentlicht wurde
def on_publish(client, userdata, mid, properties=None):
    print()  #("Message published with mid: " + str(mid))


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect
client.on_publish = on_publish

# TLS aktivieren (sichere Verbindung)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)


client.username_pw_set("NAME", "PASSOWRD")

# Mit HiveMQ-Cloud verbinden
client.connect("URL", 8883)

def load_csv_data(file_path):
    data_list = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Header überspringen
        for row in reader:
            sensor_id, sensor_type, value = row
            data_list.append(f"{sensor_id},{sensor_type},{value}")
    return data_list

def pair_data_with_timestamp(data):
    timestamp = int(time.time())
    # timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp},{data}"

def check_event(last_data, data):
    split_last_data = last_data.split(",")
    split_data = data.split(",")
    value_last_data = float(split_last_data[-1])
    value_data = float(split_data[-1]) # nehme letzen Wert (value des Sensors)
    time_value = frequent_send_temperature

    if abs(value_last_data - value_data) >= 1: #Schwankung von 1 Grad (egal ob positiv oder negativ)
        time_value = frequent_send_temperature / 5
 
    return time_value

temperature_data_list = load_csv_data('./CSV_puffer/temperature_iot_sensor_data.csv')

client.loop_start()

try:
    for i in range(len(temperature_data_list)):
        time.sleep(check_event(temperature_data_list[i-1], temperature_data_list[i]))
        client.publish("iot/sensor/data/temperature", payload=pair_data_with_timestamp(temperature_data_list[i]), qos=1)
        print(f"Sent data: {temperature_data_list[i]} \n")

except KeyboardInterrupt:
    print("Publisher stopped.")
    client.loop_stop()
