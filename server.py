"""
Servidor de Teste HTTP Simples (Python Standard Library)
-------------------------------------------------------
Este script executa um servidor web local para testes de APIs e desenvolvimento.

Como executar:
    python server.py

Acesse no navegador ou curl:
    http://localhost:8080/
    http://localhost:8080/health
    http://localhost:8080/api/info
    http://localhost:8080/api/echo (POST com JSON)
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

HOST = "localhost"
PORT = 8080

class TestServerHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status_code=200, content_type="application/json"):
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._set_headers(200, "text/html; charset=utf-8")
            html_content = """<!DOCTYPE html>
<html lang="pt-PT">
<head>
    <meta charset="UTF-8">
    <title>Servidor de Teste</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; line-height: 1.6; }
        .card { background: #f4f4f9; padding: 20px; border-radius: 8px; border-left: 4px solid #007bff; }
        code { background: #e0e0e0; padding: 2px 6px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Servidor de Teste Ativo!</h2>
        <p>O seu servidor de teste em Python está a funcionar corretamente.</p>
        <h3>Endpoints disponíveis:</h3>
        <ul>
            <li><code>GET /health</code> - Estado do servidor</li>
            <li><code>GET /api/info</code> - Informações do sistema</li>
            <li><code>POST /api/echo</code> - Envia JSON de volta</li>
        </ul>
    </div>
</body>
</html>"""
            self.wfile.write(html_content.encode("utf-8"))

        elif self.path == "/health":
            self._set_headers(200)
            response = {
                "status": "UP",
                "timestamp": datetime.now().isoformat(),
                "message": "Servidor em execução sem problemas."
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))

        elif self.path == "/api/info":
            self._set_headers(200)
            response = {
                "app": "Servidor de Testes Local",
                "version": "1.0.0",
                "environment": "test",
                "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))

        else:
            self._set_headers(404)
            response = {
                "error": 404,
                "message": f"Rota '{self.path}' não encontrada."
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_POST(self):
        if self.path == "/api/echo":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                self._set_headers(200)
                response = {
                    "status": "success",
                    "received_data": data,
                    "timestamp": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                self._set_headers(400)
                response = {
                    "status": "error",
                    "message": "JSON inválido enviado no corpo da requisição."
                }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))
        else:
            self._set_headers(404)
            response = {"error": 404, "message": "Endpoint POST não encontrado."}
            self.wfile.write(json.dumps(response, ensure_ascii=False, indent=2).encode("utf-8"))


def run():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, TestServerHandler)
    print(f" Servidor de teste a correr em http://{HOST}:{PORT}")
    print("Pressione Ctrl+C para encerrar.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n Servidor encerrado.")
        httpd.server_close()

if __name__ == "__main__":
    run()
    