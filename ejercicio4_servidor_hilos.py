# Ejercicio 4 - Servidor de eco multicliente: un hilo por conexion
import socket
import threading

PUERTO = 5000


def atender_cliente(conexion, direccion):
    """Eco con framing por \n para UN cliente (corre en su propio hilo)."""
    with conexion:
        buffer = ""
        while True:
            datos = conexion.recv(1024)
            if not datos:
                break
            buffer += datos.decode("utf-8")
            while "\n" in buffer:
                linea, buffer = buffer.split("\n", 1)
                conexion.sendall((linea + "\n").encode("utf-8"))
    print("Conexion cerrada:", direccion)


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", PUERTO))
    servidor.listen()
    print("Servidor multicliente en el puerto", PUERTO)
    while True:
        # el hilo principal SOLO acepta; cada cliente tiene su hilo
        conexion, direccion = servidor.accept()
        hilo = threading.Thread(target=atender_cliente,
                                args=(conexion, direccion),
                                daemon=True)
        hilo.start()


main()
