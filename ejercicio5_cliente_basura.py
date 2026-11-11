# Prueba del ejercicio 5: un cliente que envia basura a proposito
import socket
import time

with socket.create_connection(("127.0.0.1", 5000), timeout=5) as conexion:
    conexion.sendall(b"hola esto no es el protocolo\n")
    print("respuesta 1:", conexion.recv(1024).decode("utf-8").strip())
    conexion.sendall(b"\xff\xfe\xfa\n")  # bytes que no son UTF-8 valido
    print("respuesta 2:", conexion.recv(1024).decode("utf-8").strip())
    conexion.sendall("TURNO>valido\n".encode("utf-8"))
    print("respuesta 3:", conexion.recv(1024).decode("utf-8").strip())
    time.sleep(0.2)
