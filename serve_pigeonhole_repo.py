# Simple HTTP Server for Pigeonhole Streaming Repository
# This script serves the Pigeonhole Streaming repository files over HTTP

import http.server
import socketserver
import os

# Define the port to use
PORT = 8000

# Change to the repository directory
repo_path = r"M:\pigeonhole-streaming"
os.chdir(repo_path)

# Create the HTTP server
Handler = http.server.SimpleHTTPRequestHandler

# Start the server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving Pigeonhole Streaming repository at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")