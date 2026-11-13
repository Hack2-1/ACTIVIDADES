import requests

BASE = "https://localhost:8443"
CERT = "certificado.pem"

print("--- 1. Crear incidencias (POST) ---")
r1 = requests.post(
    f"{BASE}/incidencias",
    json={"tipo": "alerta", "descripcion": "Escaneo de puertos"},
    verify=CERT, timeout=10
)
print("POST 1:", r1.status_code, r1.json())
id_creada = r1.json()["id"]

r2 = requests.post(
    f"{BASE}/incidencias",
    json={"tipo": "vulnerabilidad", "descripcion": "SSH con contrasena debil"},
    verify=CERT, timeout=10
)
print("POST 2:", r2.status_code, r2.json())

print("\n--- 2. Probar vocabulario controlado inválido (POST 400) ---")
r_inv = requests.post(
    f"{BASE}/incidencias",
    json={"tipo": "alerta", "descripcion": "Prueba", "estado": "inventado"},
    verify=CERT, timeout=10
)
print("POST estado inválido:", r_inv.status_code, r_inv.json())

print("\n--- 3. Consultar con filtros combinados (GET) ---")
r_filtro = requests.get(
    f"{BASE}/incidencias",
    params={"tipo": "alerta", "estado": "abierta"},
    verify=CERT, timeout=10
)
print("Filtro alerta + abierta:", r_filtro.status_code, r_filtro.json())

print("\n--- 4. Modificar estado (PATCH) ---")
r_patch = requests.patch(
    f"{BASE}/incidencias/{id_creada}",
    json={"estado": "resuelta"},
    verify=CERT, timeout=10
)
print("PATCH:", r_patch.status_code, r_patch.json())

print("\n--- 5. Reemplazo completo (PUT - reinicia a abierta) ---")
r_put = requests.put(
    f"{BASE}/incidencias/{id_creada}",
    json={"tipo": "incidente", "descripcion": "Escaneo de puertos confirmado y mitigado"},
    verify=CERT, timeout=10
)
print("PUT:", r_put.status_code, r_put.json())

print("\n--- 6. Comprobar recurso inexistente (GET 404) ---")
r_404 = requests.get(f"{BASE}/incidencias/999", verify=CERT, timeout=10)
if r_404.status_code == 404:
    print("404 esperado:", r_404.json()["error"])

print("\n--- 7. Auditoría del servidor (/contadores y /logs) ---")
print("Contadores:", requests.get(f"{BASE}/contadores", verify=CERT, timeout=10).json())
print("Logs:", requests.get(f"{BASE}/logs", verify=CERT, timeout=10).json())