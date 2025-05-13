from concurrent import futures
import grpc
import sensor_pb2
import sensor_pb2_grpc
import threading
import asyncio
import websockets
import json

# --- gRPC Sensor ---
class TemperatureSensorServicer(sensor_pb2_grpc.TemperatureSensorServicer):
    def SendTemperature(self, request, context):
        print(f"[gRPC] Recibido: Sensor {request.sensor_id}, Temp: {request.temperature}°C", flush=True)
        return sensor_pb2.Acknowledgement(message="Temperatura recibida correctamente.")

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_TemperatureSensorServicer_to_server(TemperatureSensorServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC en puerto 50051...")
    server.start()
    server.wait_for_termination()

# --- Websocket Sensor ---
async def websocket_server(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print(f"[WebSocket] Recibido: Sensor {data['sensor']}, BPM: {data['value']}", flush=True)

def serve_websocket():
    async def start_server():
        print("[WebSocket] Servidor iniciado en puerto 8765")
        async with websockets.serve(websocket_server, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever

    asyncio.run(start_server())

if __name__ == '__main__':
    threading.Thread(target=serve_grpc, daemon=True).start()
    serve_websocket()
