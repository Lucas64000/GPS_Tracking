import sys

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'lucas',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

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
