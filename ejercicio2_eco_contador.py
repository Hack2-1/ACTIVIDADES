# Ejercicio 2 - Eco con contador independiente por cliente: 1>hola, 2>otro
import socket
import threading

PUERTO = 5000


def atender_cliente(conexion, direccion):
    contador = 0  # variable LOCAL: cada hilo (cliente) tiene la suya
    with conexion:
        buffer = ""
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            buffer += datos.decode("utf-8")
            while "\n" in buffer:
                linea, buffer = buffer.split("\n", 1)
                contador += 1
                respuesta = f"{contador}>{linea}\n"
                conexion.sendall(respuesta.encode("utf-8"))
    print(f"Conexion cerrada: {direccion}")


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", PUERTO))
    servidor.listen()
    print("Eco con contador en el puerto", PUERTO)
    while True:
        conexion, direccion = servidor.accept()
        threading.Thread(target=atender_cliente,
                         args=(conexion, direccion), daemon=True).start()


main()
