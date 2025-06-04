import paho.mqtt.client as mqtt
import psycopg2
import json
import os

# Configuración
MQTT_TOPIC = "iot/health_data/sensor_2"

BROKER = os.getenv("MQTT_BROKER")

POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "database": "health_data",
    "user": "iot_user",
    "password": "iot_password"
}


def on_message(client, userdata, msg):
    print(f"[Subscriber] Mensaje recibido bruto: {msg.payload}", flush=True)  # Nuevo log

    try:
        data = json.loads(msg.payload.decode())
        
        # Conexión a PostgreSQL

        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        print(f"[Subscriber] Decodificado: {data}", flush=True)
        
        valor = None 
            
        valor = data.get('data')
        id_sensor = data.get('sensor_id')
        timestamp = data.get('timestamp')
        sensor_type = data.get('sensor_type')

        cursor.execute("""
            INSERT INTO sensor_data (
                sensor_id, 
                sensor_type,
                value_sensor, 
                timestamp
            ) VALUES (%s, %s, %s, %s)
            """, (
                id_sensor,
                sensor_type,
                valor, 
                timestamp
                )
        )
        
        conn.commit()
        cursor.close()
        conn.close()

        print(f"[DB] Insertado en PostgreSQL {valor}", flush=True)


        
    except Exception as e:
        print(f"Error: {e}", flush=True)



# Configuración MQTT
client = mqtt.Client()
client.on_message = on_message
print(f"[MQTT] Conectando a broker {BROKER}...", flush=True)

client.connect(os.getenv("MQTT_BROKER"), 1883, 180)
client.subscribe(MQTT_TOPIC)
print("[MQTT] Suscrito a 'sensor2'", flush=True)
client.loop_forever()