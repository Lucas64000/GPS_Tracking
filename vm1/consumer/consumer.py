import asyncio
from fastapi import FastAPI
from kafka import KafkaConsumer
from fastapi.middleware.cors import CORSMiddleware
import threading
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez restreindre cela à des origines spécifiques si nécessaire
    allow_credentials=True,
    allow_methods=["*"],  # Ou spécifiez les méthodes autorisées (GET, POST, etc.)
    allow_headers=["*"],  # Ou spécifiez les en-têtes autorisés
)
# Nom du topic Kafka auquel le consumer va s'abonner
TOPIC_NAME = "gps"

# Adresse du broker Kafka
BROKER_URL = "broker:9093"  # C'est l'adresse que le consumer voit dans le réseau Docker


# Liste pour stocker les messages reçus
received_messages = []



# Fonction pour consommer les messages de Kafka (en arrière-plan)
def consume_messages():
    # Initialisation du consumer Kafka
    consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[BROKER_URL],
        auto_offset_reset='earliest',  # Lit les messages depuis le début du topic si aucun offset n'est défini
        enable_auto_commit=True,       # Permet de committer automatiquement les offsets
    )
    global received_messages
    for message in consumer:
        print(f"Message reçu : {message.value}")
        received_messages.append(message.value.decode('utf-8'))

# Démarrage de la fonction de consommation dans un thread en arrière-plan

@app.get("/")
def read_root():
    return {"message": "FastAPI with Kafka is running!"}

# Endpoint pour récupérer les messages consommés²
@app.get("/messages")
def get_messages():
    return {"messages": received_messages}


# Démarrer la consommation dans un thread séparé pour ne pas bloquer FastAPI
@app.on_event("startup")
def startup_event():
    # Lancer la consommation Kafka dans un thread séparé
    threading.Thread(target=consume_messages, daemon=True).start()