# Ejercicio 3 - Servidor UDP (puerto 5001): responde "servidor activo" a ESTADO
import socket

PUERTO = 5001

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(("0.0.0.0", PUERTO))  # en UDP no hay listen() ni accept()
print("Servidor UDP escuchando en el puerto", PUERTO)

while True:
    # recvfrom devuelve los datos Y la direccion de quien los envio
    datos, direccion = servidor.recvfrom(1024)
    mensaje = datos.decode("utf-8").strip()
    if mensaje == "ESTADO":
        respuesta = "servidor activo"
    else:
        respuesta = "consulta no reconocida"
    # sendto necesita el destino en cada envio
    servidor.sendto((respuesta + "\n").encode("utf-8"), direccion)
