import os

# Werte vom Nutzer abfragen
frequent_send_humidity = input("Gib das Zeitintervall für den LUFTFEUCHTIGKEITSSENSOR ein (in sekunden): ")
frequent_send_light = input("Gib das Zeitintervall für den LICHTSENSOR ein (in sekunden): ")
frequent_send_movement = input("Gib das Zeitintervall für den BEWEGUNGSSENSOR ein (in sekunden): ")
frequent_send_temperature = input("Gib das Zeitintervall für den TEMPERATURSSENSOR ein (in sekunden): ")
frequent_send_co2 = input("Gib das Zeitintervall für den CO2-SENSOR ein (in sekunden): ")


file_path = "./mqtt/time_interval.py"


with open(file_path, "w") as file:
    file.write(f"frequent_send_humidity = {frequent_send_humidity}\nfrequent_send_light = {frequent_send_light}\nfrequent_send_movement = {frequent_send_movement}\nfrequent_send_temperature = {frequent_send_temperature}\nfrequent_send_co2 = {frequent_send_co2}\n")

print(f"{file_path} wurde überschrieben.")



# Nun die anderen Skripte starten
os.system("start cmd /k python ./mqtt/mqtt_publisher_temperature.py")
os.system("start cmd /k python ./mqtt/mqtt_publisher_humidity.py")
os.system("start cmd /k python ./mqtt/mqtt_publisher_light.py")
os.system("start cmd /k python ./mqtt/mqtt_publisher_movement.py")
os.system("start cmd /k python ./mqtt/mqtt_publisher_co2.py")
os.system("start cmd /k python ./mqtt/mqtt_subscriber.py")
os.system("start cmd /k python ./mqtt/event_listener.py")
