import asyncio
import websockets
import json
import time
import random
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuración del sensor
GATEWAY_WS_URL = "ws://iot-gateway:8765/ws/presion"
SENSOR_ID = "presion_sensor_001"

def generar_presion_arterial():
    """
    Genera datos simulados de presión arterial.

    Rangos típicos:
    - Sistólica (alta): 90-140 mmHg
    - Diastólica (baja): 60-90 mmHg

    Clasificación:
    - Normal: <120/<80
    - Elevada: 120-129/<80
    - Hipertensión Estadio 1: 130-139/80-89
    - Hipertensión Estadio 2: ≥140/≥90
    - Crisis hipertensiva: >180/>120
    - Hipotensión: <90/<60
    """
    # Probabilidad de generar presión normal
    if random.random() < 0.7:  # 70% de probabilidad de presión normal
        sistolica = random.randint(110, 129)
        diastolica = random.randint(70, 84)
    else:
        # Generamos algunos casos de presión anormal
        caso = random.random()
        if caso < 0.4:  # Hipertensión Estadio 1
            sistolica = random.randint(130, 139)
            diastolica = random.randint(80, 89)
        elif caso < 0.7:  # Hipertensión Estadio 2
            sistolica = random.randint(140, 179)
            diastolica = random.randint(90, 119)
        elif caso < 0.85:  # Crisis hipertensiva (poco común)
            sistolica = random.randint(180, 200)
            diastolica = random.randint(120, 130)
        else:  # Hipotensión
            sistolica = random.randint(80, 89)
            diastolica = random.randint(50, 59)

    timestamp = int(time.time())

    return {
        "sensor_id": SENSOR_ID,
        "tipo": "presion_arterial",
        "valor": {
            "sistolica": sistolica,
            "diastolica": diastolica
        },
        "unidad": "mmHg",
        "timestamp": timestamp
    }

async def enviar_datos():
    """Envía datos del sensor al IoT Gateway usando WebSockets"""
    while True:
        try:
            async with websockets.connect(GATEWAY_WS_URL) as websocket:
                logger.info(f"Conectado a {GATEWAY_WS_URL}")

                while True:
                    # Generar datos de presión arterial
                    datos = generar_presion_arterial()

                    # Convertir a JSON y enviar
                    mensaje = json.dumps(datos)
                    await websocket.send(mensaje)
                    logger.info(f"Datos enviados: {datos}")

                    # Recibir confirmación del gateway
                    confirmacion = await websocket.recv()
                    logger.info(f"Confirmación recibida: {confirmacion}")

                    # Esperar entre 3 y 6 segundos antes de enviar el siguiente dato
                    await asyncio.sleep(random.uniform(3, 6))

        except websockets.exceptions.ConnectionClosed:
            logger.error("Conexión cerrada. Reintentando...")
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            await asyncio.sleep(5)

def main():
    # Esperar un tiempo antes de empezar a enviar datos
    # para asegurar que el gateway esté listo
    logger.info("Esperando 10 segundos para iniciar envío de datos...")
    time.sleep(10)

    logger.info(f"Iniciando sensor de presión arterial con WebSockets")
    asyncio.run(enviar_datos())

if __name__ == "__main__":
    main()
