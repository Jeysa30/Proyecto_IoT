FROM python:3.10-slim

WORKDIR /app

COPY blood_pressure_rest.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "blood_pressure_rest.py"]