import random
import time
import requests
import datetime 

# Configuración del sensor
SENSOR_ID = 2
GATEWAY_URL = "http://iot-gateway:5000"  # conexion con el endpoint rest del gateway


def generate_blood_pressure():
    """Genera datos simulados de presión arterial"""
    blood_pressure = random.randint(60, 100)  # presion arterial
    return {
        "sensor_id": SENSOR_ID,
        "blood_pressure": blood_pressure,
        "timestamp": datetime.datetime.now().isoformat()
    }

def send_to_gateway():
    """Envía datos al gateway periódicamente"""
    while True:
        try:
            data = generate_blood_pressure()
            response = requests.post(f"{GATEWAY_URL}/blood-pressure", json=data)
            print(f"[Sensor2] Datos enviados al gateway. Respuesta: {response.status_code}", flush=True)
        except Exception as e:
            print(f"Error al enviar datos al gateway: {e}")

        
        time.sleep(10)  # Enviar cada 10 segundos


if __name__ == '__main__':
    send_to_gateway()