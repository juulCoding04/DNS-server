import http.server
import socketserver

PORT = 8080
DIRECTORY = "html-files"

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/site-a.com':
            self.path = '/site-a.html'
        if self.path == '/site-b.com':
            self.path = '/site-b.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def translate_path(self, path):
        return f"./{DIRECTORY}/{path}"
    
handler = HttpRequestHandler
server = socketserver.TCPServer(("0.0.0.0", PORT), handler)

print(f"HTTP server is ready on port {PORT}")
server.serve_forever()