# Fasciculo - Seccion F (respuestas)

Las secciones A0, A, B, C, D y E ya traen su hoja de respuestas en el PDF del fasciculo.

## F1. Ciclos de vida (Codigos 1 y 2)
- (a) Bloqueo esperando cliente: `conexion, direccion = servidor.accept()`
- (b) Bloqueo esperando datos: `datos = conexion.recv(1024)`
- (c) Linea del cliente que dispara el handshake: `cliente.connect((IP_SERVIDOR, PUERTO))`

## F2. while True + funciones
Ver `F2_eco_contador_servidor.py`. Salida esperada con tres mensajes:
ECO #1> hola / ECO #2> redes / ECO #3> adios

## F3. UDP y best-effort
Al apagar el servidor y enviar otro mensaje, el cliente imprime tras 3 s:
`... silencio: el datagrama se perdio y NADIE aviso ...`
No hay error de conexion porque UDP no tiene conexion ni confirmaciones: sendto() solo entrega
el datagrama a la red y regresa sin saber si llego. El unico indicio de la perdida es que
recvfrom() no recibe nada, y eso se detecta unicamente gracias a settimeout(3).
(Captura: correr Codigo 4 del fasciculo y pegar la pantalla del cliente.)

## F4. Framing
Ver `F4_framing_cliente_tres.py`. El servidor imprime tres lineas separadas.
La linea que sabe donde termina cada mensaje es `while "\n" in buffer:` junto con
`mensaje, buffer = buffer.split("\n", 1)`: el delimitador \n marca el fin de cada mensaje.

## F5. Bloqueo
- Con ESPERA = 7 el servidor mide aproximadamente 7.0 segundos.
- Con `conexion.settimeout(5)` justo despues de accept(): a los 5 s salta `socket.timeout`
  en el SERVIDOR (el lado que esta esperando en recv()), no en el cliente.
  Se captura con try/except socket.timeout.

## F6. Codigo limpio
Ver `F6_codigo_limpio.py` (constantes en mayusculas, nombres entendibles, comentarios con el porque).
