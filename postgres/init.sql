CREATE TABLE IF NOT EXISTS sensor_data (
    temperature FLOAT,
    systolic INT,
    diastolic INT,
    heart_rate INT,
    timestamp TIMESTAMP,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);