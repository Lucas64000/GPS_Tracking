import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from kafka import KafkaConsumer
from fastapi.middleware.cors import CORSMiddleware
import threading
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://postgres:password@postgres:5432/daddy_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
Base = declarative_base()

class GPSMessage(Base):
    __tablename__ = "gps_messages"
    id = Column(Integer, primary_key=True, index=True)
    daddy_id = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

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

consumer = KafkaConsumer(
    'gps',
    bootstrap_servers=['broker:9093'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
)

def consume_kafka_messages():
    session = SessionLocal()
    try:
        for message in consumer:
            print(f"Message reçu : {message.value.decode('utf-8')}")
            message_decoded = json.loads(message.value.decode("utf-8"))
            
            gps_message = GPSMessage(
                daddy_id=message_decoded.get("id"),
                latitude=message_decoded.get("latitude"),
                longitude=message_decoded.get("longitude"),
                timestamp=datetime.utcnow()
            )
            session.add(gps_message)
            session.commit()

            if manager.active_connections:
                asyncio.run(manager.broadcast(message.value.decode("utf-8")))
    except Exception as e:
        print(f"Erreur lors de la consommation Kafka : {e}")
    finally:
        session.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI with Kafka and DB is running!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        manager.disconnect(websocket)

@app.get("/messages")
def get_saved_messages():
    session = SessionLocal()
    try:
        messages = session.query(GPSMessage).all()
        return [
            {
                "id": msg.id,
                "daddy_id": msg.daddy_id,
                "latitude": msg.latitude,
                "longitude": msg.longitude,
                "timestamp": msg.timestamp,
            }
            for msg in messages
        ]
    finally:
        session.close()

@app.on_event("startup")
def startup_event():
    threading.Thread(target=consume_kafka_messages, daemon=True).start()
