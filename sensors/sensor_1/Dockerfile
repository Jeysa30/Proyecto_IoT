FROM python:3.10-slim

WORKDIR /app

COPY sensor.proto .
COPY body_temperature_gRPC.py .
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Compila los archivos proto
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. sensor.proto

CMD ["python", "body_temperature_gRPC.py"]
