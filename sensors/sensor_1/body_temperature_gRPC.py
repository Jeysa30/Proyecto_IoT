import grpc
import time
import random
import datetime

import sensor_pb2
import sensor_pb2_grpc

SENSOR_ID = "1"

def generate_temperature():
    return round(random.uniform(36.0, 38.5), 2)

def run():
    channel = grpc.insecure_channel('iot-gateway:50051')
    stub = sensor_pb2_grpc.TemperatureSensorStub(channel)


    while True:
        temp_data = sensor_pb2.TemperatureData(
            sensor_id=SENSOR_ID,
            temperature=generate_temperature(),
            timestamp=datetime.datetime.now().isoformat()
        )

        ack = stub.SendTemperature(temp_data)
        print(f"[Sensor1] Enviado a gateway: {temp_data.temperature}°C | [Sensor1] Respuesta: {ack.message}", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    run()
