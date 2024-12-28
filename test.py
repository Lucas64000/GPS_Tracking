from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio
from kafka import KafkaConsumer
import sys
import json 

app = FastAPI()

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

# Route WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accepter la connexion WebSocket
    count = 0
    try:
        while True:
            consumer = KafkaConsumer(
                'gps',
                bootstrap_servers='localhost:9092',
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )

            print("En attente des messages...")
            for message in consumer:
                # Vérifie si le message a une valeur non nulle
                if message.value is not None:
                    try:
                        json_data = json.loads(message.value.decode('utf-8'))
                        id, lat, long = json_data.values()
                        print(str(lat))
                        await websocket.send_text(str(lat))  # Envoyer le compteur
                        await asyncio.sleep(2)  #
                    except UnicodeDecodeError as e:
                        print(f"Erreur de décodage pour le message : {e}")
                else:
                    print("Received an empty message. Skipping...")

    except WebSocketDisconnect:
        print("Client déconnecté")
