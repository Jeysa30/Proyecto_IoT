import grpc
import time
import random
from datetime import datetime

import sensor_pb2
import sensor_pb2_grpc

def generate_temperature():
    return round(random.uniform(36.0, 38.5), 2)

def run():
    channel = grpc.insecure_channel('iot-gateway:50051')
    stub = sensor_pb2_grpc.TemperatureSensorStub(channel)

    while True:
        temp_data = sensor_pb2.TemperatureData(
            sensor_id="temp_sensor_1",
            temperature=generate_temperature(),
            timestamp=datetime.utcnow().isoformat()
        )

        ack = stub.SendTemperature(temp_data)
        print(f"Enviado: {temp_data.temperature}°C | Respuesta: {ack.message}")
        time.sleep(5)

if __name__ == "__main__":
    run()
