# Ejercicio 3 - Cliente TCP que maneja todos los fallos y sale con codigo != 0
import socket
import sys

PUERTO = 5000
TIMEOUT = 5


def main():
    ip_servidor = input("IP del servidor: ").strip()
    try:
        conexion = socket.create_connection((ip_servidor, PUERTO), timeout=TIMEOUT)
    except ConnectionRefusedError:
        print("Servidor apagado: conexion rechazada")
        sys.exit(1)
    except socket.gaierror:
        print("IP o nombre invalido, no se pudo resolver:", ip_servidor)
        sys.exit(2)
    except TimeoutError:
        print("El servidor no respondio a tiempo al conectar")
        sys.exit(3)

    with conexion:
        try:
            conexion.sendall("hola\n".encode("utf-8"))
            datos = conexion.recv(1024)
            if not datos:
                print("El servidor cerro la conexion a media conversacion")
                sys.exit(4)
            print("Servidor responde:", datos.decode("utf-8").strip())
        except TimeoutError:
            print("La respuesta nunca llego")
            sys.exit(5)
        except (ConnectionResetError, BrokenPipeError):
            print("Desconexion a media conversacion")
            sys.exit(4)


main()
