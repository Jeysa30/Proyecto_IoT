import time
import random
import requests
import json
import logging
from threading import Thread

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración del sensor
GATEWAY_URL = "http://iot-gateway:8080/api/sensor/data"
SENSOR_ID = "ritmo_sensor_001"

def generar_ritmo_cardiaco():
    """
    Genera datos simulados de ritmo cardíaco

    Rangos:
    - Bradicardia: <60 lpm
    - Normal: 60-100 lpm
    - Taquicardia: >100 lpm
    """
    # Probabilidad de generar ritmo cardíaco normal
    if random.random() < 0.8:  # 80% de probabilidad de ritmo normal
        ritmo = random.randint(60, 100)
    else:
        # 10% de probabilidad de bradicardia, 10% de taquicardia
        if random.random() < 0.5:
            ritmo = random.randint(40, 59)  # Bradicardia
        else:
            ritmo = random.randint(101, 180)  # Taquicardia

    timestamp = int(time.time())

    return {
        "sensor_id": SENSOR_ID,
        "tipo": "ritmo_cardiaco",
        "valor": ritmo,
        "unidad": "lpm",  # latidos por minuto
        "timestamp": timestamp
    }

def enviar_datos():
    """Envía datos del sensor al IoT Gateway usando REST API"""
    while True:
        try:
            # Generar datos de ritmo cardíaco
            datos = generar_ritmo_cardiaco()

            # Enviar datos al gateway usando REST
            headers = {'Content-Type': 'application/json'}
            response = requests.post(GATEWAY_URL, json=datos, headers=headers)

            if response.status_code == 200:
                logger.info(f"Datos enviados correctamente: {datos}")
            else:
                logger.error(f"Error al enviar datos: {response.status_code} - {response.text}")

            # Esperar entre 1 y 3 segundos antes de enviar el siguiente dato
            time.sleep(random.uniform(1, 3))

        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión: {str(e)}")
            time.sleep(5)  # Reintentar en 5 segundos
        except Exception as e:
            logger.error(f"Error general: {str(e)}")
            time.sleep(5)  # Reintentar en 5 segundos

def health_check_server():
    """Servidor simple para verificar el estado del sensor"""
    from http.server import HTTPServer, BaseHTTPRequestHandler

    class HealthCheckHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/health':
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "healthy"}).encode())
            else:
                self.send_response(404)
                self.end_headers()

    server = HTTPServer(('0.0.0.0', 8081), HealthCheckHandler)
    logger.info("Servidor de health check iniciado en puerto 8081")
    server.serve_forever()

def main():
    # Iniciar servidor de health check en un hilo separado
    health_thread = Thread(target=health_check_server, daemon=True)
    health_thread.start()

    # Esperar un tiempo antes de empezar a enviar datos
    # para asegurar que el gateway esté listo
    logger.info("Esperando 10 segundos para iniciar envío de datos...")
    time.sleep(10)

    logger.info(f"Iniciando envío de datos de ritmo cardíaco al gateway: {GATEWAY_URL}")
    enviar_datos()

if __name__ == "__main__":
    main()
