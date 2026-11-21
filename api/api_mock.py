"""API de mentira para treinar consumo de REST com token e paginação.

Uso:   python api_mock.py            (sobe em http://localhost:8000)
Teste: curl -H "Authorization: Bearer token-treino-123" "http://localhost:8000/pedidos?page=1&per_page=10"

Regras:
  - Sem o header Authorization correto -> 401.
  - GET /pedidos?page=N&per_page=M     -> lista paginada (padrão: page=1, per_page=10).
  - GET /pedidos/<id>                  -> um pedido, ou 404 se não existir.
"""
import json
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

TOKEN = "token-treino-123"
PEDIDOS = json.loads((Path(__file__).parent / "pedidos_api.json").read_text(encoding="utf-8"))


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            return self._send(401, {"erro": "token ausente ou inválido"})
        url = urlparse(self.path)
        partes = [p for p in url.path.split("/") if p]
        if partes == ["pedidos"]:
            qs = parse_qs(url.query)
            page = max(int(qs.get("page", ["1"])[0]), 1)
            per_page = min(max(int(qs.get("per_page", ["10"])[0]), 1), 50)
            total = len(PEDIDOS)
            ini = (page - 1) * per_page
            return self._send(200, {
                "data": PEDIDOS[ini:ini + per_page],
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": math.ceil(total / per_page),
            })
        if len(partes) == 2 and partes[0] == "pedidos" and partes[1].isdigit():
            for p in PEDIDOS:
                if p["id"] == int(partes[1]):
                    return self._send(200, p)
            return self._send(404, {"erro": "pedido não encontrado"})
        return self._send(404, {"erro": "rota não encontrada"})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print("API de treino em http://localhost:8000  (token: %s)" % TOKEN)
    HTTPServer(("", 8000), Handler).serve_forever()
