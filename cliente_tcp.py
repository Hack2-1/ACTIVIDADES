# Cliente TCP de LA FILA: pide un turno
import socket

IP_SERVIDOR = "127.0.0.1"  # usar la IP real del servidor al validar entre equipos
PUERTO = 5000
APODO = input("Apodo: ")

with socket.create_connection((IP_SERVIDOR, PUERTO), timeout=5) as conexion:
    conexion.sendall(("TURNO>" + APODO + "\n").encode("utf-8"))
    print("Servidor responde:", conexion.recv(1024).decode("utf-8").strip())
