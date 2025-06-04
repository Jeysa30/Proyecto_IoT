CREATE TABLE IF NOT EXISTS sensor_data (
    log_id SERIAL PRIMARY KEY,
    sensor_id INT,
    sensor_type VARCHAR(100),
    value_sensor FLOAT,
    timestamp TIMESTAMP,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


