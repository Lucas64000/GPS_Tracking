from kafka import KafkaConsumer

# Nom du topic Kafka auquel le consumer va s'abonner
TOPIC_NAME = "gps"

# Adresse du broker Kafka
BROKER_URL = "broker:9093"  # C'est l'adresse que le consumer voit dans le réseau Docker

# Initialisation du consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[BROKER_URL],
    auto_offset_reset='earliest',  # Lit les messages depuis le début du topic si aucun offset n'est défini
    enable_auto_commit=True,       # Permet de committer automatiquement les offsets
)

print(f"Consumer connecté au topic '{TOPIC_NAME}' via le broker '{BROKER_URL}'.")

# Lecture des messages
try:
    for message in consumer:
        print(f"Message reçu : {message.value}")
except KeyboardInterrupt:
    print("\nArrêt du consumer.")
finally:
    consumer.close()
