# Practica 8 - Cliente en Python (requests) que recorre el ciclo CRUD completo
import requests

BASE = "http://localhost:8001"
TIMEOUT = 10


def mostrar(titulo, respuesta):
    """Imprime el codigo de estado y el cuerpo (si lo hay)."""
    cuerpo = respuesta.json() if respuesta.content else "(sin cuerpo)"
    print(f"{titulo}: {respuesta.status_code} {cuerpo}")


def main():
    # Crear: los datos van en el cuerpo (json=)
    r = requests.post(f"{BASE}/incidencias",
                      json={"tipo": "alerta", "descripcion": "Escaneo de puertos"},
                      timeout=TIMEOUT)
    mostrar("POST", r)
    creada = r.json()

    # Consultar: el filtro va en la URL (params=)
    r = requests.get(f"{BASE}/incidencias", params={"tipo": "alerta"}, timeout=TIMEOUT)
    mostrar("GET tipo=alerta", r)

    # Filtros combinados (ejercicio 5)
    r = requests.get(f"{BASE}/incidencias",
                     params={"tipo": "alerta", "estado": "abierta"}, timeout=TIMEOUT)
    mostrar("GET tipo=alerta&estado=abierta", r)

    # Modificar: id en la ruta, cambios en el cuerpo
    r = requests.patch(f"{BASE}/incidencias/{creada['id']}",
                       json={"estado": "resuelta"}, timeout=TIMEOUT)
    mostrar("PATCH", r)

    # Estado invalido (ejercicio 1)
    r = requests.patch(f"{BASE}/incidencias/{creada['id']}",
                       json={"estado": "cerrada"}, timeout=TIMEOUT)
    mostrar("PATCH estado invalido", r)

    # Reemplazo completo (ejercicio 4)
    r = requests.put(f"{BASE}/incidencias/{creada['id']}",
                     json={"tipo": "incidente", "descripcion": "Reemplazada"},
                     timeout=TIMEOUT)
    mostrar("PUT", r)

    # Comprobar el codigo antes de usar el cuerpo
    r = requests.get(f"{BASE}/incidencias/999", timeout=TIMEOUT)
    if r.status_code == 404:
        print("no existe:", r.json()["error"])

    # Eliminar
    r = requests.delete(f"{BASE}/incidencias/{creada['id']}", timeout=TIMEOUT)
    mostrar("DELETE", r)

    # La auditoria del servidor, desde fuera
    print("contadores:", requests.get(f"{BASE}/contadores", timeout=TIMEOUT).json())
    print("logs:", requests.get(f"{BASE}/logs", timeout=TIMEOUT).json())


try:
    main()
except requests.exceptions.ConnectionError:
    print("No se pudo conectar: arranque primero servidor_bitacora.py")
