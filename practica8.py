import http.server, json, time, ssl
from urllib.parse import urlparse, parse_qs

ARCHIVO = "incidencias.json"
siguiente_id = 1
logs = []
contadores = {
    "peticiones_totales": 0,
    "por_metodo": {"GET": 0, "POST": 0, "PATCH": 0, "DELETE": 0, "HEAD": 0, "PUT": 0},
    "por_familia": {"2xx": 0, "4xx": 0, "5xx": 0},
    "incidencias_por_tipo": {"alerta": 0, "vulnerabilidad": 0, "incidente": 0},
}
estados_validos = ("abierta", "en_proceso", "resuelta")

def cargar():
    """Lee las incidencias del archivo JSON al arrancar el servidor."""
    global siguiente_id
    try:
        with open(ARCHIVO, encoding="utf-8") as f:
            datos = json.load(f)
            if datos:
                siguiente_id = max(i["id"] for i in datos) + 1
            return datos
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar():
    """Reescribe el archivo JSON con la lista actual de incidencias."""
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(incidencias, f, ensure_ascii=False, indent=2)

incidencias = cargar()

class Manejador(http.server.BaseHTTPRequestHandler):
    def _leer_json(self):
        """Lee el cuerpo de la petición y lo interpreta como JSON."""
        try:
            tam = int(self.headers.get("Content-Length", 0))
            return json.loads(self.rfile.read(tam).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            return None

    def _enviar(self, codigo, datos=None):
        """Envía la respuesta JSON y anota la petición en logs y contadores."""
        cuerpo = b"" if datos is None else json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        
        if self.command != "HEAD":
            self.wfile.write(cuerpo)
            logs.append({
                "hora": time.strftime("%H:%M:%S"),
                "metodo": self.command,
                "ruta": self.path,
                "codigo": codigo
            })
            contadores["peticiones_totales"] += 1
            contadores["por_metodo"][self.command] = contadores["por_metodo"].get(self.command, 0) + 1
            contadores["por_familia"][f"{codigo // 100}xx"] += 1

    def do_HEAD(self):
        url = urlparse(self.path)
        if url.path in ("/", "/incidencias", "/logs", "/contadores"):
            self._enviar(200)
        else:
            self._enviar(404)

    def do_GET(self):
        url = urlparse(self.path)
        parametros = parse_qs(url.query)
        
        if url.path == "/":
            self._enviar(200, {
                "servicio": "Bitácora de incidencias",
                "rutas": [
                    "GET /incidencias", "GET /incidencias/<id>",
                    "POST /incidencias", "PATCH /incidencias/<id>",
                    "PUT /incidencias/<id>", "DELETE /incidencias/<id>",
                    "GET /logs", "GET /contadores"
                ],
            })
        elif url.path == "/incidencias":
            lista = incidencias
            if "tipo" in parametros:
                lista = [i for i in lista if i["tipo"] == parametros["tipo"][0]]
            if "estado" in parametros:
                lista = [i for i in lista if i["estado"] == parametros["estado"][0]]
            self._enviar(200, lista)
        elif url.path.startswith("/incidencias/"):
            try:
                buscado = int(url.path.split("/")[2])
            except ValueError:
                self._enviar(400, {"error": "id debe ser entero"})
                return
            for inc in incidencias:
                if inc["id"] == buscado:
                    self._enviar(200, inc)
                    return
            self._enviar(404, {"error": f"incidencia {buscado} no encontrada"})
        elif url.path == "/logs":
            self._enviar(200, logs)
        elif url.path == "/contadores":
            self._enviar(200, contadores)
        else:
            self._enviar(404, {"error": f"ruta no conocida: {url.path}"})

    def do_POST(self):
        url = urlparse(self.path)
        if url.path != "/incidencias":
            self._enviar(404, {"error": f"ruta no conocida: {url.path}"})
            return
        datos = self._leer_json()
        if not isinstance(datos, dict):
            self._enviar(400, {"error": "el cuerpo debe ser JSON válido"})
            return
        
        faltan = [c for c in ("tipo", "descripcion") if c not in datos]
        if faltan:
            self._enviar(400, {"error": f"faltan campos: {', '.join(faltan)}"})
            return
            
        estado_input = str(datos.get("estado", "abierta"))
        if estado_input not in estados_validos:
            self._enviar(400, {"error": f"Estado inválido. Valores válidos: {', '.join(estados_validos)}"})
            return

        global siguiente_id
        incidencia = {
            "id": siguiente_id,
            "tipo": str(datos["tipo"]),
            "descripcion": str(datos["descripcion"]),
            "estado": estado_input,
            "hora": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        siguiente_id += 1
        incidencias.append(incidencia)
        
        contadores["incidencias_por_tipo"][incidencia["tipo"]] = (
            contadores["incidencias_por_tipo"].get(incidencia["tipo"], 0) + 1
        )
        guardar()
        self._enviar(201, incidencia)

    def do_PATCH(self):
        url = urlparse(self.path)
        if not url.path.startswith("/incidencias/"):
            self._enviar(404, {"error": f"ruta no conocida: {url.path}"})
            return
        try:
            buscado = int(url.path.split("/")[2])
        except ValueError:
            self._enviar(400, {"error": "id debe ser entero"})
            return
            
        datos = self._leer_json()
        if not isinstance(datos, dict):
            self._enviar(400, {"error": "el cuerpo debe ser JSON válido"})
            return
            
        if "estado" in datos and str(datos["estado"]) not in estados_validos:
            self._enviar(400, {"error": f"Estado inválido. Valores válidos: {', '.join(estados_validos)}"})
            return

        for inc in incidencias:
            if inc["id"] == buscado:
                for campo in ("tipo", "descripcion", "estado"):
                    if campo in datos:
                        inc[campo] = str(datos[campo])
                guardar()
                self._enviar(200, inc)
                return
        self._enviar(404, {"error": f"incidencia {buscado} no encontrada"})

    def do_PUT(self):
        url = urlparse(self.path)
        if not url.path.startswith("/incidencias/"):
            self._enviar(404, {"error": f"ruta no conocida: {url.path}"})
            return
        try:
            buscado = int(url.path.split("/")[2])
        except ValueError:
            self._enviar(400, {"error": "id debe ser entero"})
            return
            
        datos = self._leer_json()
        if not isinstance(datos, dict):
            self._enviar(400, {"error": "el cuerpo debe ser JSON válido"})
            return
            
        faltan = [c for c in ("tipo", "descripcion") if c not in datos]
        if faltan:
            self._enviar(400, {"error": f"faltan campos: {', '.join(faltan)}"})
            return

        for inc in incidencias:
            if inc["id"] == buscado:
                inc["tipo"] = str(datos["tipo"])
                inc["descripcion"] = str(datos["descripcion"])
                inc["estado"] = "abierta"
                guardar()
                self._enviar(200, inc)
                return
        self._enviar(404, {"error": f"incidencia {buscado} no encontrada"})

    def do_DELETE(self):
        url = urlparse(self.path)
        if not url.path.startswith("/incidencias/"):
            self._enviar(404, {"error": f"ruta no conocida: {url.path}"})
            return
        try:
            buscado = int(url.path.split("/")[2])
        except ValueError:
            self._enviar(400, {"error": "id debe ser entero"})
            return
            
        for i, inc in enumerate(incidencias):
            if inc["id"] == buscado:
                del incidencias[i]
                guardar()
                self._enviar(204)
                return
        self._enviar(404, {"error": f"incidencia {buscado} no encontrada"})

    def log_message(self, formato, *args):
        pass

if __name__ == "__main__":
    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexto.load_cert_chain("certificado.pem", "llave.pem")
    
    servidor = http.server.HTTPServer(("localhost", 8443), Manejador)
    servidor.socket = contexto.wrap_socket(servidor.socket, server_side=True)
    print("Bitácora HTTPS en https://localhost:8443")
    servidor.serve_forever()