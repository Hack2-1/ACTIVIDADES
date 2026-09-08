import socket

# Crear socket (socket)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociar a IP y puerto 5050 (bind)
servidor.bind(('10.208.128.116', 5050))

# Esperar conexiones (listen)
servidor.listen(1)
print("Defensor esperando en puerto 5050...")

# Aceptar conexión bloqueante (accept)
conexion, direccion = servidor.accept()
print(f"Atacante conectado desde {direccion}")

while True:
    # Recibir petición y decodificar (receive = decode)
    ataque = conexion.recv(1024).decode('utf-8')
    if not ataque:
        break
    
    print(f"Ataque recibido en coordenada: {ataque}")
    
    # Enviar respuesta y codificar (send = encode)
    respuesta = input("Ingresar respuesta (AGUA/TOCADO): ")
    conexion.send(respuesta.encode('utf-8'))

conexion.close()
    
