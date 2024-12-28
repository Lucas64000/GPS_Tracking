from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kafka import KafkaProducer
from pydantic import BaseModel

class Message(BaseModel):
    message: str
# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration du producteur Kafka
producer = KafkaProducer(bootstrap_servers='broker:9093')

# Configuration de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Permet toutes les origines (à restreindre en production)
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les headers
)

@app.get("/")
def read_root():
    return {"message": "FastAPI with Kafka is running!"}


@app.post("/send")
async def send_message(msg: Message):
    
    # Envoie le message au sujet Kafka 'gps'
    producer.send('gps', value=msg.message.encode('utf-8'))
    producer.flush()
    return {"status": "Message sent to Kafka"}