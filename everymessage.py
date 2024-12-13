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
# producer.send('lucas', 'Test message'.encode('utf-8'))
# producer.flush()

# Lecture et affichage des messages (décodage en string)
print("En attente des messages...")
for message in consumer:
    # Vérifie si le message a une valeur non nulle
    if message.value is not None:
        try:
            print(f"Received message: {message.value.decode('utf-8')}")
        except UnicodeDecodeError as e:
            print(f"Erreur de décodage pour le message : {e}")
    else:
        print("Received an empty message. Skipping...")