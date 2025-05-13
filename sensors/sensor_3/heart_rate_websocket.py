import asyncio
import websockets
import random
import json

async def send_heart_rate():
    uri = "ws://iot-gateway:8765"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    heart_rate = random.randint(60, 100)
                    data = {
                        "sensor": "heart_rate",
                        "value": heart_rate
                    }
                    await websocket.send(json.dumps(data))
                    print(f"[Sensor] Enviado: {data}", flush=True)
                    await asyncio.sleep(2)
        except Exception as e:
            print(f"[Sensor] Error de conexión: {e}, reintentando en 3 segundos...", flush=True)
            await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(send_heart_rate())
