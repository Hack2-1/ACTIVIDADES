import socket
import threading

TCP_PORT = 5000
UDP_PORT = 5001
LOCK = threading.Lock()
TURN_COUNT = 0


def handle_tcp_client(connection):
    """Asigna un turno a un cliente TCP y cierra la conexión."""
    global TURN_COUNT
    try:
        request = connection.recv(4096).decode("utf-8").strip()
        if request != "TURNO":
            connection.sendall(b"ERROR\n")
            return

        with LOCK:
            TURN_COUNT += 1
            turn = TURN_COUNT

        connection.sendall(f"TURNO>{turn}\n".encode("utf-8"))
    except (ConnectionError, UnicodeError, OSError):
        pass
    finally:
        connection.close()


def handle_udp_queries():
    """Responde consultas de cuántos turnos se han repartido."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.bind(("0.0.0.0", UDP_PORT))
        while True:
            try:
                message, address = udp_socket.recvfrom(4096)
                request = message.decode("utf-8").strip()
                if request == "CUANTOS":
                    with LOCK:
                        total = TURN_COUNT
                    response = f"VAN>{total}\n".encode("utf-8")
                    udp_socket.sendto(response, address)
            except (ConnectionError, UnicodeError, OSError):
                continue


def main():
    """Inicia el servidor TCP y el hilo de consultas UDP."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind(("0.0.0.0", TCP_PORT))
        tcp_socket.listen(5)

        udp_thread = threading.Thread(target=handle_udp_queries, daemon=True)
        udp_thread.start()
        print(f"Servidor de turnos en TCP {TCP_PORT} y UDP {UDP_PORT}...")

        while True:
            try:
                connection, _ = tcp_socket.accept()
                client_thread = threading.Thread(
                    target=handle_tcp_client,
                    args=(connection,),
                    daemon=True,
                )
                client_thread.start()
            except OSError:
                break
            except KeyboardInterrupt:
                print("\nServidor detenido.")
                break


if __name__ == "__main__":
    main()
