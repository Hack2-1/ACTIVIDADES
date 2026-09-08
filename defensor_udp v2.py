import socket

# Coordenadas definidas de la flota
BARCOS = {"A1", "A2", "B3", "C4"}

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(('0.0.0.0', 5050))

print("Defensor UDP activo en 5050. Esperando datagramas...")

while True:
    datos, direccion = servidor.recvfrom(1024)
    coordenada = datos.decode('utf-8').strip().upper()

    if coordenada in BARCOS:
        respuesta = "TOCADO"
        BARCOS.remove(coordenada)
    else:
        respuesta = "AGUA"

    print(f"Ataque: {coordenada} desde {direccion} | Evaluación: {respuesta} | Barcos restantes: {len(BARCOS)}")
    servidor.sendto(respuesta.encode('utf-8'), direccion)
