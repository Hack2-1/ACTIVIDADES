# Cliente UDP de LA FILA: pregunta cuantos turnos van
import socket

DESTINO = ("127.0.0.1", 5001)  # usar la IP real del servidor entre equipos

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
    cliente.settimeout(3)
    cliente.sendto("CUANTOS".encode("utf-8"), DESTINO)
    try:
        datos, _ = cliente.recvfrom(1024)
        print("Servidor responde:", datos.decode("utf-8").strip())
    except socket.timeout:
        print("El servidor no respondio")
