# Ejercicio 2 - Cliente TCP: envia tres mensajes y muestra cada respuesta
import socket

IP_SERVIDOR = "127.0.0.1"
PUERTO = 5000
MENSAJES = ("hola", "redes", "adios")

with socket.create_connection((IP_SERVIDOR, PUERTO)) as conexion:
    for mensaje in MENSAJES:
        conexion.sendall((mensaje + "\n").encode("utf-8"))  # ENVIAR = ENCODE
        respuesta = conexion.recv(1024).decode("utf-8").strip()  # RECIBIR = DECODE
        print("Servidor responde:", respuesta)
