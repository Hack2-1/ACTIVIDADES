# Practica 8 - Servidor HTTP con CRUD en JSON (bitacora de incidencias)

Archivos: `servidor_bitacora.py` (puerto 8001) y `cliente_bitacora.py` (requests).
Ejecucion: `python3 servidor_bitacora.py` en una terminal y `python3 cliente_bitacora.py` en otra.
Dependencia del cliente: `pip install requests`.

## Resumen del diseno
| Operacion | Metodo | Ruta | Codigos |
|---|---|---|---|
| Crear | POST | /incidencias | 201, 400 |
| Leer | GET | /incidencias, /incidencias/<id>, filtros ?tipo=&estado= | 200, 400, 404 |
| Actualizar parcial | PATCH | /incidencias/<id> | 200, 400, 404 |
| Reemplazar | PUT | /incidencias/<id> | 200, 400, 404 |
| Borrar | DELETE | /incidencias/<id> | 204, 404 |
| Auditoria | GET | /logs, /contadores | 200 |

Los datos viven en `incidencias.json`; `logs` y `contadores` viven en memoria.

## Ejercicio 1 - Vocabulario controlado
La constante `ESTADOS_VALIDOS` y el metodo `_estado_invalido()` validan el campo `estado` en POST y
PATCH. Un valor distinto de abierta, en_proceso o resuelta responde 400 con la lista de validos:
`{"error": "estado invalido; valores validos: abierta, en_proceso, resuelta"}`.
Prueba: `curl -i -X PATCH http://localhost:8001/incidencias/1 -H "Content-Type: application/json" -d "{\"estado\": \"cerrada\"}"`

## Ejercicio 2 - La libreta en disco
Verificacion: crear dos incidencias, abrir `incidencias.json`, detener con Ctrl+C, reiniciar y pedir
`GET /incidencias`: siguen ahi y el siguiente id continua (`cargar()` calcula `max(id) + 1`).
**Por que /logs y /contadores vuelven a cero:** son variables en memoria (`logs = []` y el diccionario
`contadores`). Al detener el proceso la memoria se libera y al arrancar se crean vacias. Solo
`incidencias` se escribe en disco con `guardar()`, y por eso solo ella sobrevive al reinicio.

## Ejercicio 3 - El 501 invisible
Antes de implementar `do_PUT`, la clase base `BaseHTTPRequestHandler` no encuentra un metodo `do_PUT`
y ella misma genera la respuesta 501 con `send_error()`. Esa respuesta no pasa por nuestra funcion
`_enviar`, que es la unica que escribe en `logs` y actualiza `contadores`. Lo unico que aparece es el
mensaje por defecto de la biblioteca en la terminal del servidor (y aqui `log_message` esta silenciado
por nosotros para el resto de las rutas). Moraleja: lo que no pasa por `_enviar` no se audita.

## Ejercicio 4 - do_PUT
Implementado en `servidor_bitacora.py`: el id viene en la ruta, el cuerpo debe traer `tipo` y
`descripcion` (si falta alguno, 400), conserva el id original, reinicia `estado` a `abierta`, llama a
`guardar()` y responde 200 con el registro. Como ahora responde con `_enviar`, el PUT aparece en
`/contadores` (`por_metodo.PUT`), en `/logs` y en el archivo.

## Ejercicio 5 - Filtros combinados
`GET /incidencias?tipo=alerta&estado=abierta` aplica ambos filtros en cadena sobre la lista.
Pruebas: `?tipo=alerta`, `?estado=abierta`, `?tipo=alerta&estado=abierta`, `?tipo=x&estado=y` (lista vacia).
En Python: `requests.get(url, params={"tipo": "alerta", "estado": "abierta"})`.

## Evidencia
Ejecutar el servidor y el cliente y pegar aqui la salida de la terminal (el cliente imprime cada codigo
de estado y los contadores finales).
