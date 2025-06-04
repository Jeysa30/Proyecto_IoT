import asyncio
import websockets
import random
import json
import datetime

async def send_heart_rate():
    uri = "ws://iot-gateway:8765"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    heart_rate = random.randint(60, 100)
                    data = {
                        "sensor_id": "3",
                        "value": heart_rate,
                        "timestamp": datetime.datetime.now().isoformat()
                    }
                    await websocket.send(json.dumps(data))
                    print(f"[Sensor3] Enviado a gateway: {data}", flush=True)
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"[Sensor3] Error de conexión: {e}, reintentando en 3 segundos...", flush=True)
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(send_heart_rate())
