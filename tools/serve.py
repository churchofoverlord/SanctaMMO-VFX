"""Servidor local dos protótipos: http://localhost:8766

Como o `python -m http.server`, mas envia os HTML/JS/CSS com charset UTF-8 (senão os acentos saem trocados)
e sem cache, para um simples F5 mostrar sempre a versão mais recente.
Uso:  python tools/serve.py   [porta]
"""
import http.server, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8766

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
                      '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8',
                      '.md': 'text/markdown; charset=utf-8', '.txt': 'text/plain; charset=utf-8'}
    def __init__(self, *a, **k): super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def log_message(self, *a): pass

if __name__ == '__main__':
    print(f'SanctaMMO VFX em http://localhost:{PORT}/')
    http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
