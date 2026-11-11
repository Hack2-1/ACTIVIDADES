# Ejercicio 3 - Cliente UDP: consulta ESTADO esperando a lo mas 3 segundos
import socket

DESTINO = ("127.0.0.1", 5001)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
    cliente.settimeout(3)  # UDP no retransmite: el timeout detecta la perdida
    cliente.sendto("ESTADO\n".encode("utf-8"), DESTINO)
    try:
        datos, _ = cliente.recvfrom(1024)
        print("Servidor responde:", datos.decode("utf-8").strip())
    except socket.timeout:
        print("Sin respuesta en 3 segundos")
