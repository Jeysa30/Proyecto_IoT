from concurrent import futures
import grpc
import sensor_pb2
import sensor_pb2_grpc
from flask import Flask, request, jsonify
import threading
import asyncio
import websockets
import json

### GRPC ###

class TemperatureSensorServicer(sensor_pb2_grpc.TemperatureSensorServicer):
    def SendTemperature(self, request, context):
        #print(f"[gRPC] Recibido: Sensor {request.sensor_id}, Temp: {request.temperature}°C")
        print(f"[gRPC] Received from {request.sensor_id}: {request.temperature}°C at {request.timestamp}", flush=True)
        return sensor_pb2.Acknowledgement(message="Temperatura recibida correctamente.")

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_TemperatureSensorServicer_to_server(TemperatureSensorServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC en puerto 50051...")
    server.start()
    server.wait_for_termination()

### REST ### 

# Configuración del servidor REST
rest_app = Flask(__name__)

@rest_app.route('/blood-pressure', methods=['POST'])

def handle_blood_pressure():
    data = request.json
    print(f"[REST] Received blood pressure data: {data}", flush=True)
    return jsonify({"status": "success", "message": "Blood pressure data received"})


@rest_app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

def serve_rest():
    rest_app.run(host='0.0.0.0', port=5000)

### WEBSOCKET ###

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
    # Iniciar servidores en hilos separados
    import threading
    
    grpc_thread = threading.Thread(target=serve_grpc, daemon=True)
    rest_thread = threading.Thread(target=serve_rest, daemon=True)
    websocket_thread = threading.Thread(target=serve_websocket, daemon=True)
    
    grpc_thread.start()
    rest_thread.start()
    websocket_thread.start()
    
    grpc_thread.join()
    rest_thread.join()
    websocket_thread.join()