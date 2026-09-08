import socket

# Crear socket (socket)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor (connect)
cliente.connect(('10.208.128.116', 5050))

while True:
    # Enviar petición y codificar (send = encode)
    ataque = input("Ingresar coordenada de ataque (ej. B4): ")
    if not ataque:
        break
    cliente.send(ataque.encode('utf-8'))

    # Recibir respuesta y decodificar (receive = decode)
    respuesta = cliente.recv(1024).decode('utf-8')
    print(f"Respuesta del defensor: {respuesta}")

cliente.close()
