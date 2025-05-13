import paho.mqtt.client as mqtt
import psycopg2
import json
import os

# Configuración
MQTT_TOPIC = "iot/health_data"
POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": "health_data",
    "user": "iot_user",
    "password": "iot_password"
}

def on_message(client, userdata, msg):
    print(f"Mensaje recibido bruto: {msg.payload}")  # Nuevo log

    try:
        data = json.loads(msg.payload.decode())
        
        # Conexión a PostgreSQL
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        print(f"Decodificado: {data}")
        
        # Insertar datos (ajusta según tu esquema)
        cursor.execute("""
            INSERT INTO sensor_data (
                temperature, 
                blood_pressure, 
                heart_rate, 
                timestamp
            ) VALUES (%s, %s, %s, %s)
            """, (
                data.get("avg_temperature"),
                data.get("blood_pressure"),
                data.get("heart_rate"),
                data.get("timestamp")
            ))

        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

# Configuración MQTT
client = mqtt.Client()
client.connect(os.getenv("MQTT_BROKER"), 1883)
client.subscribe(MQTT_TOPIC)
client.on_message = on_message

print("Subscriptor MQTT -> PostgreSQL iniciado...")
client.loop_forever()