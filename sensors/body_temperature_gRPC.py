import time
import random
import grpc
import json
from concurrent import futures
import logging

# Importamos el archivo proto compilado
import sensor_pb2
import sensor_pb2_grpc

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Clase para implementar el servicio definido en el proto
class TemperaturaService(sensor_pb2_grpc.SensorServiceServicer):
    def SendData(self, request, context):
        logger.info(f"Recibida solicitud para enviar datos de temperatura")
        return sensor_pb2.DataResponse(status="OK")

# Función para generar datos de temperatura corporal simulados
def generar_temperatura():
    # Temperatura corporal normal entre 36.1°C y 37.5°C
    temperatura = round(random.uniform(36.1, 37.5), 1)

    # Ocasionalmente generar valores anormales (fiebre o hipotermia)
    if random.random() < 0.05:  # 5% de probabilidad de temperatura anormal
        if random.random() < 0.5:
            # Fiebre: 37.6°C - 40°C
            temperatura = round(random.uniform(37.6, 40.0), 1)
        else:
            # Hipotermia leve: 35°C - 36°C
            temperatura = round(random.uniform(35.0, 36.0), 1)

    timestamp = int(time.time())

    return {
        "sensor_id": "temp_sensor_001",
        "tipo": "temperatura_corporal",
        "valor": temperatura,
        "unidad": "celsius",
        "timestamp": timestamp
    }

def enviar_datos_temperatura(stub):
    while True:
        try:
            # Generar datos de temperatura
            datos = generar_temperatura()

            # Convertir a JSON para enviar a través de gRPC
            datos_json = json.dumps(datos)

            # Crear solicitud gRPC
            request = sensor_pb2.SensorData(sensor_type="temperatura", data=datos_json)

            # Enviar datos al servidor
            response = stub.SendData(request)

            logger.info(f"Datos enviados: {datos} - Respuesta: {response.status}")

            # Esperar entre 2 y 5 segundos antes de enviar el siguiente dato
            time.sleep(random.uniform(2, 5))

        except grpc.RpcError as e:
            logger.error(f"Error RPC: {e.code()}: {e.details()}")
            time.sleep(5)  # Reintentar en 5 segundos
        except Exception as e:
            logger.error(f"Error general: {str(e)}")
            time.sleep(5)  # Reintentar en 5 segundos

def iniciar_servidor():
    # Iniciar servidor gRPC para recibir solicitudes de configuración o control
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServiceServicer_to_server(TemperaturaService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Servidor iniciado en puerto 50051")
    return server

def main():
    # Iniciar el servidor gRPC
    servidor = iniciar_servidor()

    # Conectar al IoT Gateway
    channel = grpc.insecure_channel('iot-gateway:50051')
    stub = sensor_pb2_grpc.SensorServiceStub(channel)

    try:
        # Iniciar envío de datos
        logger.info("Iniciando envío de datos de temperatura corporal...")
        enviar_datos_temperatura(stub)
    except KeyboardInterrupt:
        servidor.stop(0)
        logger.info("Sensor de temperatura detenido")

if __name__ == "__main__":
    main()
