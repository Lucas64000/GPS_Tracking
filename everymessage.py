import sys

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer, KafkaProducer

# Création d'un consommateur Kafka
consumer = KafkaConsumer(
    'lucas',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# Création d'un producteur Kafka
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Envoi d'un message (encodage explicite en bytes)
#producer.send('quickstart-events', 'Test message'.encode('utf-8'))
#producer.flush()

# Lecture et affichage des messages (décodage en string)
print("En attente des messages...")
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")
