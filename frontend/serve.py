#!/usr/bin/env python3
import http.server
import socketserver
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = 8003
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"🌐 Frontend server running on http://localhost:{PORT}")
    print(f"📂 Serving from: {os.getcwd()}")
    print("Press CTRL+C to stop...")
    httpd.serve_forever()
