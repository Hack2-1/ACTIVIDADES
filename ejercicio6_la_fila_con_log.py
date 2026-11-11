# Ejercicio 6 - LA FILA tolerante con registro de errores en archivo
import socket
import threading
import time

PUERTO_TCP = 5000
PUERTO_UDP = 5001
PREFIJO_TURNO = b"TURNO>"
ARCHIVO_LOG = "errores.log"

turnos_asignados = 0
candado = threading.Lock()  # protege el contador compartido (seccion critica)
candado_log = threading.Lock()  # evita lineas mezcladas si dos hilos registran a la vez


def registrar_error(direccion, descripcion):
    """Escribe una linea: fecha hora (ip, puerto) descripcion."""
    marca = time.strftime("%Y-%m-%d %H:%M:%S")
    linea = f"{marca} {direccion} {descripcion}\n"
    with candado_log:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
    print(linea.strip())


def tomar_turno():
    """Incrementa el contador de forma atomica y devuelve el turno."""
    global turnos_asignados
    with candado:
        turnos_asignados += 1
        return turnos_asignados


def total_asignado():
    with candado:
        return turnos_asignados


def procesar_linea(linea):
    """Valida TURNO>apodo y arma la respuesta; None si no cumple el protocolo."""
    if not linea.startswith(PREFIJO_TURNO):
        return None
    return "turno>" + str(tomar_turno()) + "\n"


def atender_cliente_tcp(conexion, direccion):
    try:
        with conexion:
            buffer = b""  # se acumulan BYTES; se decodifica solo la linea completa
            while True:
                datos = conexion.recv(1024)
                if not datos:
                    break
                buffer += datos
                while b"\n" in buffer:
                    linea, buffer = buffer.split(b"\n", 1)
                    try:
                        linea.decode("utf-8")  # primero valida UTF-8: asi no se gasta un turno
                        respuesta = procesar_linea(linea.strip())
                    except UnicodeDecodeError:
                        registrar_error(direccion, "bytes que no son UTF-8")
                        respuesta = None
                    if respuesta is None:
                        registrar_error(direccion, "mensaje fuera de protocolo")
                        respuesta = "error>protocolo\n"
                    conexion.sendall(respuesta.encode("utf-8"))
    except (ConnectionResetError, BrokenPipeError):
        registrar_error(direccion, "conexion reiniciada por el cliente")
    finally:
        print("Conexion cerrada:", direccion)


def ciclo_tcp():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", PUERTO_TCP))
    servidor.listen()
    print("LA FILA TCP en el puerto", PUERTO_TCP)
    while True:
        conexion, direccion = servidor.accept()
        threading.Thread(target=atender_cliente_tcp,
                         args=(conexion, direccion), daemon=True).start()


def ciclo_udp():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind(("0.0.0.0", PUERTO_UDP))
    print("LA FILA UDP en el puerto", PUERTO_UDP)
    while True:
        try:
            datos, direccion = servidor.recvfrom(1024)
            if datos.decode("utf-8").strip() == "CUANTOS":
                respuesta = "van>" + str(total_asignado()) + "\n"
            else:
                respuesta = "error>consulta\n"
            servidor.sendto(respuesta.encode("utf-8"), direccion)
        except UnicodeDecodeError:
            registrar_error(("udp", 0), "datagrama no UTF-8 descartado")
        except OSError as error:
            registrar_error(("udp", 0), f"error UDP ignorado: {error}")


def main():
    threading.Thread(target=ciclo_udp, daemon=True).start()
    ciclo_tcp()  # el hilo principal atiende el ciclo TCP


main()
