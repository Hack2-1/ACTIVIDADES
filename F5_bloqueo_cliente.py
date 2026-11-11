# F5 - Cliente que calla 7 segundos antes de enviar
import socket
import time

PUERTO = 5199
ESPERA = 7  # segundos de silencio

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("localhost", PUERTO))
print("cliente> conectado; callo", ESPERA, "segundos...")
time.sleep(ESPERA)
try:
    cliente.send("ya llegue!".encode("utf-8"))
except OSError:
    print("cliente> el servidor ya cerro la conexion")
cliente.close()
