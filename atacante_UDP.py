import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor_destino = ('127.0.0.1', 5050)

while True:
    ataque = input("Coordenada de disparo: ")
    if not ataque:
        break
    cliente.sendto(ataque.encode('utf-8'), servidor_destino)
    respuesta, _ = cliente.recvfrom(1024)
    print(f"Respuesta recibida: {respuesta.decode('utf-8')}")

cliente.close()
