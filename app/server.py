from __future__ import annotations

import argparse
import http.server
import json
import ssl
from datetime import UTC, datetime


class LabHandler(http.server.BaseHTTPRequestHandler):
    server_version = "IPOGTLSLab/1.0"

    def do_GET(self) -> None:
        if self.path == "/":
            self._send_json(
                {
                    "message": "Servidor do lab TLS respondendo.",
                    "scheme": "https" if isinstance(self.request, ssl.SSLSocket) else "http",
                    "client": self.client_address[0],
                    "timestamp": datetime.now(UTC).isoformat(),
                }
            )
            return

        if self.path == "/health":
            self._send_json({"status": "ok"})
            return

        self.send_error(404, "Rota nao encontrada")

    def log_message(self, format: str, *args: object) -> None:
        print(f"{self.address_string()} - {format % args}")

    def _send_json(self, payload: dict[str, str]) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def build_server(host: str, port: int, certfile: str | None, keyfile: str | None) -> http.server.HTTPServer:
    server = http.server.ThreadingHTTPServer((host, port), LabHandler)
    if certfile and keyfile:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        server.socket = context.wrap_socket(server.socket, server_side=True)
    return server


def main() -> None:
    parser = argparse.ArgumentParser(description="Servidor HTTP/HTTPS didatico para o lab TLS.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--certfile")
    parser.add_argument("--keyfile")
    args = parser.parse_args()

    server = build_server(args.host, args.port, args.certfile, args.keyfile)
    scheme = "https" if args.certfile and args.keyfile else "http"
    print(f"Servidor {scheme.upper()} ouvindo em {scheme}://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
