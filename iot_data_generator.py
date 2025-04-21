import random
import csv

amount_dataset = 500
current_humidity = 50.0
temperature = 25.5  # Starttemperatur
temperature_file_path = f"./CSV_puffer/temperature_iot_sensor_data.csv"
humidity_file_path = f"./CSV_puffer/humidity_iot_sensor_data.csv"
light_file_path = f"./CSV_puffer/light_iot_sensor_data.csv"
movement_file_path = f"./CSV_puffer/movement_iot_sensor_data.csv"
co2_file_path = f"./CSV_puffer/co2_iot_sensor_data.csv"


# Funktion zur Generierung von Wärmedaten
def generate_temperature():
    #temperature = 25.5  # Starttemperatur
    global temperature
    change = random.choice([1, -1])  # Zufällige Richtung (steigend oder fallend)
    
    if random.random() <= 0.05:  # Zufallszahl zwischen 0 und 1, 5% Chance für Werte ≤ 0.05
        temperature += random.uniform(1.1, 2.0) * change  # Größere Änderung zwischen 1.1 und 2.0
    else:
        temperature += random.uniform(0.1, 0.3) * change  # Normale Änderung zwischen 0.1 und 0.3

    if temperature > 31.0: # zu warm -> Klimaanlage angeschaltet
        temperature -= 3.0
    
    if temperature < 20.5: # zu kalt -> Heizung angeschaltet
        temperature += 3.0
    
    return round(temperature, 2)


def generate_humidity():
    global current_humidity

    if current_humidity < 40:
        current_humidity += 4.5
    if current_humidity > 60:
        current_humidity -= 4.5

    # Kleine, natürliche Schwankungen
    change = random.uniform(-2.5, 2.5)
    current_humidity += change

    # Begrenzung der Werte auf einen realistischen Bereich
    current_humidity = max(20, min(current_humidity, 80))

    # Seltene, abrupte Änderungen (5% Wahrscheinlichkeit)
    if random.random() <= 0.05:
        if random.random() <= 0.5:
            # Plötzlicher Abfall
            current_humidity -= random.uniform(5, 10)
        else:
            # Plötzlicher Anstieg 
            current_humidity += random.uniform(5, 10)
        current_humidity = max(20, min(current_humidity, 80))  # Begrenzung beibehalten

    return round(current_humidity, 2)


def generate_light():
    lux = 0
    if random.random() <= 0.05:
        lux = round(random.uniform(300, 400), 2) 
    else:
        lux = 0
    return lux

def generate_movement():
    movement = 0
    if random.random() <= 0.05:
        movement = 1
    return movement

def generate_co2():
    co2 = 0
    if random.random() <= 0.05:
        co2 = round(random.uniform(1001, 2100), 2)
    else:
        co2 = 0
    return co2




with open(temperature_file_path, 'w', newline='') as file:
    writer = csv.writer(file)

    for _ in range(amount_dataset):
        writer.writerow(["TEMP_BuildingA_Floor3_Room305","celsius", generate_temperature()])


with open(humidity_file_path, 'w', newline='') as file:
    writer = csv.writer(file)

    for _ in range(amount_dataset):
        writer.writerow(["HUMID_BuildingA_Floor3_Room305","%", generate_humidity()])


with open(light_file_path, 'w', newline='') as file:
    writer = csv.writer(file)

    for _ in range(amount_dataset):
        writer.writerow(["LIGHT_BuildingA_Floor3_Room305","lux", generate_light()])


with open(movement_file_path, 'w', newline='') as file:
    writer = csv.writer(file)

    for _ in range(amount_dataset):
        writer.writerow(["MOVE_BuildingA_Floor3_Room305","movement", generate_movement()])


with open(co2_file_path, 'w', newline='') as file:
    writer = csv.writer(file)

    for _ in range(amount_dataset):
        writer.writerow(["CO2_BuildingA_Floor3_Room305","ppm", generate_co2()])

