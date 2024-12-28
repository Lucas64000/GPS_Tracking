import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from kafka import KafkaConsumer
from fastapi.middleware.cors import CORSMiddleware
import threading
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Vous pouvez restreindre cela à des origines spécifiques si nécessaire
    allow_credentials=True,
    allow_methods=["*"],  # Ou spécifiez les méthodes autorisées (GET, POST, etc.)
    allow_headers=["*"],  # Ou spécifiez les en-têtes autorisés
)
# Nom du topic Kafka auquel le consumer va s'abonner
TOPIC_NAME = "gps"

# Adresse du broker Kafka
BROKER_URL = "broker:9093"  # C'est l'adresse que le consumer voit dans le réseau Docker


# WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Liste pour stocker les messages reçus
received_messages = []
active_connections = []

consumer = KafkaConsumer(
        TOPIC_NAME,
        bootstrap_servers=[BROKER_URL],
        auto_offset_reset='earliest',  # Lit les messages depuis le début du topic si aucun offset n'est défini
        enable_auto_commit=True,       # Permet de committer automatiquement les offsets
    )

# Fonction pour consommer les messages de Kafka (en arrière-plan)
def consume_kafka_messages():
    for message in consumer:
        print(f"Message reçu : {message.value.decode('utf-8')}")
        # Diffuser le message à toutes les connexions WebSocket
        message_decoded = message.value.decode("utf-8")
        if manager.active_connections:
            import asyncio
            asyncio.run(manager.broadcast(message_decoded))
# Démarrage de la fonction de consommation dans un thread en arrière-plan

@app.get("/")
def read_root():
    return {"message": "FastAPI with Kafka is running!"}

# Endpoint pour récupérer les messages consommés²
@app.get("/messages")
def get_messages():
    return {"messages": received_messages}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Here, we don't need to do anything with the incoming messages from the client
            # The server just listens for Kafka messages and broadcasts them to the client
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        manager.disconnect(websocket)

        
# Démarrer la consommation dans un thread séparé pour ne pas bloquer FastAPI
@app.on_event("startup")
def startup_event():
    threading.Thread(target=consume_kafka_messages, daemon=True).start()