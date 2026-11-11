# Ejercicio 1 - Servidor TCP de eco con framing por \n (puerto 5000)
import socket

PUERTO = 5000
TAMANO_LECTURA = 1024

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# permite reutilizar el puerto despues de reiniciar el servidor
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind(("0.0.0.0", PUERTO))
servidor.listen(1)
print("Servidor eco escuchando en el puerto", PUERTO)

# accept() BLOQUEA hasta que llegue un cliente
conexion, direccion = servidor.accept()
print("Cliente conectado:", direccion)

buffer = ""  # aqui se acumula lo recibido: TCP es un flujo de bytes
while True:
    datos = conexion.recv(TAMANO_LECTURA)
    if not datos:  # recv() vacio = el cliente cerro
        break
    buffer += datos.decode("utf-8")
    # cada \n marca un mensaje completo
    while "\n" in buffer:
        linea, buffer = buffer.split("\n", 1)
        conexion.sendall((linea + "\n").encode("utf-8"))

conexion.close()
servidor.close()
print("Servidor terminado.")
