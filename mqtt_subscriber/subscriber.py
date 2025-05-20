import paho.mqtt.client as mqtt
import psycopg2
import json
import os

# Configuración
MQTT_TOPIC = "iot/health_data"

BROKER = os.getenv("MQTT_BROKER")

POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "database": "health_data",
    "user": "iot_user",
    "password": "iot_password"
}

def on_message(client, userdata, msg):
    print(f"Mensaje recibido bruto: {msg.payload}", flush=True)  # Nuevo log

    try:
        data = json.loads(msg.payload.decode())
        
        # Conexión a PostgreSQL

        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        print(f"Decodificado: {data}", flush=True)
        
        temperature = data.get("avg_temperature"),
        systolic = data.get("last_blood_pressure", {}).get("systolic"),
        diastolic = data.get("last_blood_pressure", {}).get("diastolic"),                    
        heart_rate = data.get("last_blood_pressure", {}).get("heart_rate"),
        timestamp = data.get("timestamp")
        # Insertar datos (ajusta según tu esquema)
        cursor.execute("""
            INSERT INTO sensor_data (
                temperature, 
                systolic, 
                diastolic, 
                heart_rate, 
                timestamp
            ) VALUES (%s, %s, %s, %s, %s)
            """, (
                temperature, 
                systolic, 
                diastolic, 
                heart_rate, 
                timestamp
                )
        )
        
        conn.commit()
        cursor.close()
        conn.close()

        print(f"[DB] Insertado en PostgreSQL {temperature}", flush=True)


        
    except Exception as e:
        print(f"Error: {e}", flush=True)


# Configuración MQTT
client = mqtt.Client()
client.on_message = on_message
print(f"[MQTT] Conectando a broker {BROKER}...", flush=True)

client.connect(os.getenv("MQTT_BROKER"), 1883, 180)
client.subscribe(MQTT_TOPIC)
print("[MQTT] Suscrito a 'sensor/data'", flush=True)
client.loop_forever()