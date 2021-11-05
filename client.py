import socket
from sys import exit
import errno

# CONSTANTS
HEADERSIZE = 10


try:
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print("Socket successfuly created")
except socket.error as err:
    print(f"Socket creation failed with error {err}")

# Default host and port for socket
HOST = "raspberrypi"
PORT = 8000

# Connect to server
try:
    c.connect((HOST, PORT))
    # print("Successfully connected to server.")
except ConnectionRefusedError:
    print("[ERRNO 111] Connection refused")
    exit()
except OSError as e:
    if e.errno == errno.ENOTCONN:
        print(e)
        exit()
    else:
        print("Something went wrong with connecting to host")
        exit()


while True:

    full_msg = ""
    new_msg = True

    while True:
        # Look for keyboard interrupts
        try:
            server_msg = c.recv(16)
        except KeyboardInterrupt:
            print("Successfully left the program")
            c.close()
            exit()

        if new_msg and server_msg != b'':
            print(f"new message length: {server_msg[:HEADERSIZE]}")
            msglen = int(server_msg[:HEADERSIZE])
            new_msg = False

        full_msg += server_msg.decode("utf-8")

        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg received")
            print(full_msg[HEADERSIZE:])

            # Quit program
            print("Press CTRL+C to cancel")

            new_msg = True
            full_msg = ""

    print(full_msg)
