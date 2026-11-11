# LA FILA version RPC (XML-RPC): sin una sola linea de sockets
import threading
from socketserver import ThreadingMixIn
from xmlrpc.server import SimpleXMLRPCServer

PUERTO = 5000

turnos_asignados = 0
candado = threading.Lock()  # protege el contador compartido


class ServidorHilos(ThreadingMixIn, SimpleXMLRPCServer):
    """XML-RPC atendiendo cada llamada en su propio hilo."""
    daemon_threads = True


def tomar_turno(apodo):
    """Devuelve el siguiente turno (consecutivo, sin repeticiones)."""
    global turnos_asignados
    with candado:
        turnos_asignados += 1
        turno = turnos_asignados
    print("Turno", turno, "para", apodo)
    return turno


def cuantos_van():
    """Devuelve el total de turnos asignados."""
    with candado:
        return turnos_asignados


servidor = ServidorHilos(("0.0.0.0", PUERTO), allow_none=True, logRequests=False)
servidor.register_function(tomar_turno, "tomar_turno")
servidor.register_function(cuantos_van, "cuantos_van")
print("LA FILA RPC en el puerto", PUERTO, "...")
servidor.serve_forever()
