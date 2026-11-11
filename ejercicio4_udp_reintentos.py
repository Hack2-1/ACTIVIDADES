# Ejercicio 4 - CUANTOS por UDP con reintentos y espera creciente (1, 2 y 4 s)
import socket
import time

DESTINO = ("127.0.0.1", 5001)
REINTENTOS = 3
TIMEOUT_RESPUESTA = 2


def consultar(servidor, mensaje, reintentos=REINTENTOS):
    """Envia la consulta y reintenta; devuelve None si se agotan los intentos."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        cliente.settimeout(TIMEOUT_RESPUESTA)
        for intento in range(1, reintentos + 1):
            try:
                cliente.sendto((mensaje + "\n").encode("utf-8"), servidor)
                datos, _ = cliente.recvfrom(1024)
                return datos.decode("utf-8").strip()
            except TimeoutError:
                espera = 2 ** (intento - 1)  # 1, 2, 4 segundos
                print(f"Intento {intento}: sin respuesta, espero {espera} s")
                time.sleep(espera)
    return None


respuesta = consultar(DESTINO, "CUANTOS")
print(respuesta if respuesta else "El servidor no respondio")
