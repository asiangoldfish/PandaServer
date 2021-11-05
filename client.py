import socket
import sys

try:
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfuly created")
except socket.error as err:
    print(f"Socket creation failed with error {err}")

# Default host and port for socket
HOST = "192.168.1.170"
PORT = 8000

# Connect to server
try:
    c.connect((HOST, PORT))
    print("Successfully connected to server.")
except ConnectionRefusedError:
    print("[ERRNO 111] Connection refused")
