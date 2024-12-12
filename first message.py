import sys

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer, KafkaProducer

# Création d'un consommateur Kafka
consumer = KafkaConsumer(
    'quickstart-events',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group'
)

# Création d'un producteur Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Envoi d'un message (encodage explicite en bytes)
producer.send('quickstart-events', 'Test message'.encode('utf-8'))
producer.flush()

# Lecture et affichage des messages (décodage en string)
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")
    break
