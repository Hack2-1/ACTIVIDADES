# Cliente RPC de LA FILA: ServerProxy es el stub
import xmlrpc.client

DIRECCION = "http://localhost:5000"

servidor = xmlrpc.client.ServerProxy(DIRECCION)
apodo = input("Apodo: ")
turno = servidor.tomar_turno(apodo)
print("Tu turno es:", turno)
print("Turnos asignados hasta ahora:", servidor.cuantos_van())
