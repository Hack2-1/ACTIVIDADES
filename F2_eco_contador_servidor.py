# F2 - Servidor de eco con contador y funcion armar_eco
import socket

PUERTO = 5050


def armar_eco(mensaje, numero):
    """Devuelve el eco numerado: ECO #N> mensaje"""
    return "ECO #" + str(numero) + "> " + mensaje


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", PUERTO))
servidor.listen(1)
print("Servidor eco con contador en el puerto", PUERTO)

# accept() BLOQUEA hasta que llegue un cliente
conexion, direccion = servidor.accept()
print("Cliente conectado desde", direccion)

contador = 0
while True:
    datos = conexion.recv(1024)
    if not datos:  # b'' significa que el cliente cerro
        break
    contador += 1
    mensaje = datos.decode("utf-8")
    print("Me llego:", mensaje)
    conexion.send(armar_eco(mensaje, contador).encode("utf-8"))

conexion.close()
servidor.close()
print("Servidor terminado.")
