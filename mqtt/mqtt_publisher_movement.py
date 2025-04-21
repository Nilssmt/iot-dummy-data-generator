import time
import csv
import random
import paho.mqtt.client as paho
from paho import mqtt
from time_interval import frequent_send_movement

frequent_data_send = frequent_send_movement # damit variable global zugreifbar ist
def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))

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
    #timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp},{data}"

def check_event(data):
    split_data = data.split(",")
    value_data = float(split_data[-1]) # nehme letzen Wert (value des Sensors)
 
    return value_data

movement_data_list = load_csv_data('./CSV_puffer/movement_iot_sensor_data.csv')


client.loop_start()


try:
    for i in range(len(movement_data_list)):
        if check_event(movement_data_list[i]) == 1:
            client.publish("iot/sensor/data/movement", payload=pair_data_with_timestamp(movement_data_list[i]), qos=1)
            frequent_data_send = random.uniform(frequent_send_movement - (frequent_send_movement * 0.3), frequent_send_movement + (frequent_send_movement * 0.3)) # damit bewegung nicht immer gleichen frequenz hat
        print(f"Sent data: {movement_data_list[i]} \n")
        time.sleep(frequent_data_send)

except KeyboardInterrupt:
    print("Publisher stopped.")
    client.loop_stop()
