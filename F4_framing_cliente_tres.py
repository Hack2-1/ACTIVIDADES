# F4 - Cliente que envia TRES mensajes en un solo send()
# Usar con framing_servidor.py (Codigo 5 del fasciculo, puerto 5061)
import socket

PUERTO = 5061

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("localhost", PUERTO))

# Tres mensajes juntos: el servidor debe separarlos por el delimitador \n
cliente.send("primer mensaje\nsegundo mensaje\ntercer mensaje\n".encode("utf-8"))
cliente.close()
