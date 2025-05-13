CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    temperature REAL,
    blood_pressure REAL,
    heart_rate INTEGER,
    timestamp TIMESTAMPTZ NOT NULL
);