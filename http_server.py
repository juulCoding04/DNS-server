import http.server
import socketserver

PORT = 8080
DIRECTORY = "html-files"

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get('Host', '')

        if 'a.com' in host:
            self.path = '/a.html'
        elif 'b.com' in host:
            self.path = '/b.html'
        else:
            self.path = '/'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def translate_path(self, path):
        resolved_path = f"./{DIRECTORY}/{path.lstrip('/')}"
        print(f"Translating path: {path} -> {resolved_path}")
        return resolved_path
    
handler = HttpRequestHandler
server = socketserver.TCPServer(("0.0.0.0", PORT), handler)

print(f"HTTP server is ready on port {PORT}")
server.serve_forever()