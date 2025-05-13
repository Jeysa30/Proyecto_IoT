from concurrent import futures
import grpc
import sensor_pb2
import sensor_pb2_grpc

class TemperatureSensorServicer(sensor_pb2_grpc.TemperatureSensorServicer):
    def SendTemperature(self, request, context):
        #print(f"[gRPC] Recibido: Sensor {request.sensor_id}, Temp: {request.temperature}°C")
        print(f"[gRPC] Received from {request.sensor_id}: {request.temperature}°C at {request.timestamp}", flush=True)
        return sensor_pb2.Acknowledgement(message="Temperatura recibida correctamente.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_TemperatureSensorServicer_to_server(TemperatureSensorServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Servidor gRPC en puerto 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
