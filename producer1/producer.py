import sys
import random
import json
from time import sleep
import os

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer, KafkaProducer

# Création d'un producteur Kafka
ipbroker = os.getenv('IP_BROKER')
producer = KafkaProducer(bootstrap_servers=[f'{ipbroker}:9092'])
lat, long = 43.3, -0.37

while(True):
    randomLatitude = random.uniform(-0.001, 0.001)
    randomLongitude = random.uniform(-0.001, 0.001)
    id = 1
    lat += randomLatitude
    long += randomLongitude

    coordinates = {"id": id, "latitude": lat, "longitude": long}
    message = json.dumps(coordinates).encode('utf-8')
    producer.send('gps', message)
    producer.flush()
    sleep(1)