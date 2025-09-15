import requests
from requests.auth import HTTPBasicAuth

# Test basic HTTP connection
url = "http://192.168.1.130:8080/jsonrpc"
auth = HTTPBasicAuth("kodi", "0000")

try:
    # Simple ping test
    response = requests.get("http://192.168.1.130:8080", auth=auth, timeout=5)
    print(f"Basic HTTP response: {response.status_code}")

    # JSON-RPC test
    payload = {
        "jsonrpc": "2.0",
        "method": "JSONRPC.Ping",
        "id": 1
    }

    response = requests.post(url, json=payload, auth=auth, timeout=5)
    print(f"JSON-RPC response: {response.status_code}")
    print(f"Response text: {response.text}")

except Exception as e:
    print(f"Connection error: {e}")

# Also test if port 8080 is open
import socket
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex(("192.168.1.130", 8080))
    sock.close()
    if result == 0:
        print("Port 8080 is open")
    else:
        print("Port 8080 is not accessible")
except Exception as e:
    print(f"Socket error: {e}")