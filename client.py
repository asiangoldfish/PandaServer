import socket
from sys import exit
import errno

# Used for handling Python objects in bytes
import pickle

# CONSTANTS
HEADERSIZE = 10


try:
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print("Socket successfuly created")
except socket.error as err:
    print(f"Socket creation failed with error {err}")

# DEVELOPMENT ONLY
# Please change this code block and for the variable HOST before deployment
HOST = ""
while True:
    try:
        print("""
        Press 1 to connect to localhost
        Press 2 to connect to 192.168.1.170
        Press 3 to connect to raspberrypi
        Press 4 to connect to raspberrypi.local
        Press CTRL + C to cancel and exit the program.
        \nYour selection is : """, end="")
        prompt_host = input()

    except KeyboardInterrupt:
        print("\nSuccessfully exit the program!")
        exit()
    else:
        prompt_switcher = {
            "1": "localhost",
            "2": "192.168.1.170",
            "3": "raspberrypi",
            "4": "raspberrypi.local",
        }
        break


# Default host and port for socket
HOST = prompt_switcher.get(prompt_host)
PORT = 8000

# Checks if HOST is valid
if HOST is None:
    print("Please select a valid host.")
    exit()

# Connect to server
try:
    print("Connecting to %s..." % HOST)
    c.connect((HOST, PORT))
    # print("Successfully connected to server.")
except ConnectionRefusedError:
    print("Connection refused")
    exit()
except socket.gaierror:
    print("Cannot find host. Host is invalid or not available.")
    exit()
except OSError as e:
    if e.errno == errno.ENOTCONN:
        print(e)
        exit()
    else:
        print("Something went wrong with connecting to host.")
        exit()

while True:
    # Look for keyboard interrupts
    try:
        server_msg = c.recv(16)
    except KeyboardInterrupt:
        print("Successfully left the program")
        c.close()
        exit()
    except OSError as e:
        print(e)
        exit()

        # Quit program
        print("\nPress CTRL+C to terminate the program.")
    
    print(server_msg.decode())
    break
