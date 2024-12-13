import sys
import random
import json
from time import sleep


if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer, KafkaProducer

# Création d'un consommateur Kafka
# consumer = KafkaConsumer(
#     'lucas',
#     bootstrap_servers=['localhost:9092'],
#     auto_offset_reset='earliest',
#     enable_auto_commit=True
# )

# Création d'un producteur Kafka
producer = KafkaProducer(bootstrap_servers=['192.168.69.184:9092'])
lat, long = 43.3, -0.37

while(True):
    randomLatitude = random.uniform(-0.001, 0.001)
    randomLongitude = random.uniform(-0.001, 0.001)
    id = 2
    lat += randomLatitude
    long += randomLongitude

    coordinates = {"id": id, "latitude": lat, "longitude": long}
    message = json.dumps(coordinates).encode('utf-8')
    producer.send('lucas', message)
    producer.flush()
    sleep(1)


# Envoi d'un message (encodage explicite en bytes)


# producer.flush()

# Lecture et affichage des messages (décodage en string)
# print("En attente des messages...")
# for message in consumer:
#     # Vérifie si le message a une valeur non nulle
#     if message.value is not None:
#         try:
#             print(f"Received message: {message.value.decode('utf-8')}")
#         except UnicodeDecodeError as e:
#             print(f"Erreur de décodage pour le message : {e}")
#     else:
#         print("Received an empty message. Skipping...")