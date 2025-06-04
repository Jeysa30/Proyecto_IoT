import paho.mqtt.client as mqtt
from concurrent import futures
import grpc
import sensor_pb2
import sensor_pb2_grpc
from flask import Flask, request, jsonify
import threading
import asyncio
import websockets
import json
import datetime 

### GRPC ###

class TemperatureSensorServicer(sensor_pb2_grpc.TemperatureSensorServicer):
    def SendTemperature(self, request, context):
        print(f"[gRPC] Temperatura recibida de {request.sensor_id}: {request.temperature}°C a las {request.timestamp}", flush=True)
        #ensor_data["temperature"].append(request.temperature)
        publish_to_mqtt("temperature", request.sensor_id, request.temperature, request.timestamp, "iot/health_data/sensor_1")
        return sensor_pb2.Acknowledgement(message="Temperatura recibida correctamente.")

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_TemperatureSensorServicer_to_server(TemperatureSensorServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("[RPC] Servidor iniciado en puerto 50051")
    server.start()
    server.wait_for_termination()

### REST ### 

# Configuración del servidor REST
rest_app = Flask(__name__)

@rest_app.route('/blood-pressure', methods=['POST'])

def handle_blood_pressure():
    data = request.json
    print(f"[REST] Presion arterial recibida: {data}", flush=True)
    #sensor_data["blood_pressure"].append(data)
    publish_to_mqtt("blood_pressure", data['sensor_id'], data['blood_pressure'], data['timestamp'], "iot/health_data/sensor_2")
    return jsonify({"status": "success", "message": "Blood pressure data received"})


def serve_rest():
    rest_app.run(host='0.0.0.0', port=5000)
    print("[REST] Servidor iniciado en puerto 5000")

### WEBSOCKET ###

# --- Websocket Sensor ---
async def websocket_server(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print(f"[WebSocket] Frecuencia cardianca recibida de: Sensor {data['sensor_id']}, BPM: {data['value']}", flush=True)
        publish_to_mqtt("heart_rate", data['sensor_id'], data['value'], data['timestamp'], "iot/health_data/sensor_3")

def serve_websocket():
    async def start_server():
        print("[WebSocket] Servidor iniciado en puerto 8765")
        async with websockets.serve(websocket_server, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever

    asyncio.run(start_server())

### MQTT ###
# --- Configuración MQTT ---
MQTT_BROKER = "mosquitto"  # Nombre del servicio en Docker
MQTT_PORT = 1883



# --- Cliente MQTT ---
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 180)

### --- MQTT: Publicar --- ###
def publish_to_mqtt(sensor_type, sensor_id, data, timestamp, topic):
    message = {
        "sensor_type": sensor_type,
        "sensor_id": sensor_id,
        "data": data,
        "timestamp": timestamp
    }

    message_json = json.dumps(message)
    print(f"[MQTT] Publicando mensaje a tópico '{topic}': {message_json}")

    try:
        mqtt_client.publish(
            topic=topic,
            payload=message_json
        )
        print("[MQTT] Mensaje publicado correctamente")

    except Exception as e:
        print(f"[ERROR] Falló publicación MQTT: {e}", flush=True)





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