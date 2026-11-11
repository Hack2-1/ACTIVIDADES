# F6 - Version limpia del codigo original
import socket

PUERTO = 9000
TAMANO_LECTURA = 1024

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SO_REUSEADDR evita "Address already in use" al reiniciar el servidor
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("localhost", PUERTO))
servidor.listen(1)

# accept() devuelve un socket NUEVO para hablar con este cliente
conexion, direccion = servidor.accept()
datos = conexion.recv(TAMANO_LECTURA)
print("Me llego:", datos.decode("utf-8"))

conexion.close()
servidor.close()
