# Discusion de cierre: llamar una funcion que no existe
import xmlrpc.client

servidor = xmlrpc.client.ServerProxy("http://localhost:5000")
try:
    servidor.funcion_que_no_existe()
except xmlrpc.client.Fault as error:
    print("Llego una Fault:", error.faultCode, error.faultString)
