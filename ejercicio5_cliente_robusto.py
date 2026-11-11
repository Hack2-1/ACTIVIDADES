# Ejercicio 5a - Cliente TCP con mensajes claros para cada fallo
import socket
import sys

IP_SERVIDOR = "127.0.0.1"
PUERTO = 5000
MENSAJES = ("hola", "redes", "adios")


def main():
    try:
        conexion = socket.create_connection((IP_SERVIDOR, PUERTO), timeout=5)
    except ConnectionRefusedError:
        print("El servidor esta apagado (conexion rechazada)")
        sys.exit(1)
    except socket.gaierror:
        print("La IP o el nombre no se pudo resolver:", IP_SERVIDOR)
        sys.exit(1)
    except TimeoutError:
        print("El servidor no respondio a tiempo")
        sys.exit(1)

    with conexion:
        try:
            for mensaje in MENSAJES:
                conexion.sendall((mensaje + "\n").encode("utf-8"))
                datos = conexion.recv(1024)
                if not datos:
                    print("El servidor cerro la conexion a media conversacion")
                    sys.exit(1)
                print("Servidor responde:", datos.decode("utf-8").strip())
        except (ConnectionResetError, BrokenPipeError):
            print("El servidor se fue a media conversacion")
            sys.exit(1)
        except TimeoutError:
            print("La respuesta nunca llego")
            sys.exit(1)


main()
