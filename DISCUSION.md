# Discusion de cierre - LA FILA version RPC

**Que paso con el servicio UDP de CUANTOS?**
Ya no hace falta. La consulta ahora es la funcion `cuantos_van()` y viaja como cualquier
llamada RPC: XML dentro de una peticion HTTP, que por debajo va sobre TCP.

**Que se gano y que se perdio respecto a sockets?**
- Se gano: cero codigo de sockets, encode/decode ni framing; el protocolo (nombres de funciones,
  argumentos, tipos) lo da el middleware; llamar al servidor se siente como llamar una funcion local
  (transparencia de acceso); los errores del servidor llegan como excepciones.
- Se perdio: control fino del protocolo y de los bytes; eficiencia (XML es verboso y HTTP agrega
  encabezados); la ligereza de UDP para consultas simples; y se corre el riesgo de olvidar que
  cada llamada cruza la red, tarda mas y puede fallar.

**Llamar una funcion que no existe: que excepcion llega y donde se genera?**
Llega `xmlrpc.client.Fault` en el CLIENTE, pero se genera en el SERVIDOR: el skeleton no
encuentra el metodo registrado, empaca el error como una respuesta `<fault>` y el stub del cliente
lo desempaca y lo lanza como excepcion. Ver `prueba_funcion_inexistente.py`.
