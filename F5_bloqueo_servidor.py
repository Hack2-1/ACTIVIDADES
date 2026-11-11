# F5 - Bloqueo: medir la espera y probar settimeout
# Primera corrida: TIMEOUT_RECV = None (sin limite) con ESPERA = 7 en el cliente.
# Segunda corrida: TIMEOUT_RECV = 5 -> salta socket.timeout en el SERVIDOR.
import socket
import time

PUERTO = 5199
TIMEOUT_RECV = None  # cambiar a 5 para la segunda parte

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("localhost", PUERTO))
servidor.listen(1)
print("servidor> esperando conexion...")
conexion, direccion = servidor.accept()
conexion.settimeout(TIMEOUT_RECV)  # justo despues de accept()
print("servidor> cliente conectado:", direccion)

inicio = time.time()
try:
    datos = conexion.recv(1024)  # aqui ocurre el bloqueo
    espera = time.time() - inicio
    print("servidor> recv() regreso despues de {:.1f} segundos".format(espera))
    print("servidor> llego:", datos.decode("utf-8"))
except socket.timeout:
    espera = time.time() - inicio
    print("servidor> socket.timeout despues de {:.1f} segundos".format(espera))
finally:
    conexion.close()
    servidor.close()
