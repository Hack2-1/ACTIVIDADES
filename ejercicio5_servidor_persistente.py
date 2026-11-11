# Ejercicio 5b - Servidor multicliente que sobrevive a desconexiones abruptas
import socket
import threading

PUERTO = 5000


def atender_cliente(conexion, direccion):
    """El try/except vive AQUI: el fallo de un cliente solo mata a su hilo."""
    try:
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
    except ConnectionResetError:
        print("El cliente", direccion, "se desconecto abruptamente")
    except BrokenPipeError:
        print("No se pudo enviar al cliente", direccion)
    except UnicodeDecodeError:
        print("El cliente", direccion, "envio bytes que no son UTF-8")
    finally:
        print("Conexion cerrada:", direccion)  # siempre se registra


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        servidor.bind(("0.0.0.0", PUERTO))
    except OSError:
        print("El puerto", PUERTO, "esta ocupado por otro proceso")
        return
    servidor.listen()
    print("Servidor persistente en el puerto", PUERTO)
    while True:
        conexion, direccion = servidor.accept()
        threading.Thread(target=atender_cliente,
                         args=(conexion, direccion),
                         daemon=True).start()


main()
