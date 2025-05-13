FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
COPY heart_rate_websocket.py .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "heart_rate_websocket.py"]
