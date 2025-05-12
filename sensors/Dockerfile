# Imagen base de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requerimientos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos de código fuente
COPY *.py /app/
COPY *.proto /app/

# Compilar el archivo proto para gRPC
RUN python -m pip install grpcio-tools && \
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. sensor.proto

# Variables de entorno predeterminadas
ENV PYTHONUNBUFFERED=1

# El comando para ejecutar se especificará en el docker-compose
CMD ["python", "temperatura_corporal_grpc.py"]
