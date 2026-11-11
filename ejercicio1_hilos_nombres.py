# Ejercicio 1 - Tres hilos cuyos nombres y saludos salen de una lista de tuplas
import threading
import time

PARTICIPANTES = [("Ana", 3), ("Beto", 5), ("Cora", 2)]


def saludar(nombre, cantidad):
    """Imprime 'cantidad' saludos con una pausa de un segundo."""
    for numero in range(cantidad):
        print(f"{nombre}: hola {numero}")
        time.sleep(1)


def main():
    hilos = []
    for nombre, cantidad in PARTICIPANTES:
        hilo = threading.Thread(target=saludar, args=(nombre, cantidad))
        hilos.append(hilo)
        hilo.start()
    # segundo ciclo: join() a cada hilo para que el mensaje final salga al final
    for hilo in hilos:
        hilo.join()
    print("Fin del programa")


main()
