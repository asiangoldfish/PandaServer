import socket

from sys import exit
import errno
import os

# Used for handling Python objects in bytes
import pickle
from typing import Type

from mysql.connector import connect, Error


class SystemCheck:
    """
    Run system check to make sure there are no errors upon running the server. Provides methods to enable
    or disable use of database.
    """

    def __init__(self):
        self.enable_db = False

    def set_db(self, switch: bool):
        """
        Choose between enabling or disabling the use of database. When enabled, server admin is prompted
        with login.

        Args:
        -----
            switch (bool): Enable or disable use of database
        """
        # Raise error if not is not passed by programmer
        if not isinstance(switch, bool):
            raise TypeError(
                "Unable to activate or deactivate database. Value must be bool, not %s." % str(type(switch)))

    def run_system_check(self):
        self. self_enable_db()


syschk = SystemCheck()
syschk.set_db(True)

# Connect to MySQL database only if login credentials are valid
print("Running system checks...")
print("Logging into MySQL...")
try:
    # Temporary solution
    mydb = connect(
        host="localhost",
        user="test_user",
        password="test_user123",
        database="panda",
    )
    print("\nSuccessfully logged into MYSQL!")
    print("Detected unsafe login. Please only use this method for development.")

# Quit program if wrong login credentials
except Error as error:
    print(error)
    exit()

print("\nSystem checks complete!")

# CONSTANTS
HOST = ""  # Listens to requests coming from the network
"""try:
    PORT = int(input("Enter port number: "))
except KeyboardInterrupt:
    print("\nTerminating the program.")
    exit()"""
PORT = 8080
HEADERSIZE = 10

# Create IPv4 TCP socket if permission is there
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enables reuse of socket
old_state = server_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)

print("\nSocket successfully created")

# Enable the SO_REUSE ADDR option
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
new_state = server_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)

# Bind socket to host and port
try:
    server_socket.bind((HOST, PORT))
except PermissionError as e:
    # Permission denied
    if e.errno == errno.EACCES:
        print("%s most likely due to port number %i" % (e.strerror, PORT))
        exit()
    else:
        print("Something went wrong when binding socket to port and host")
        exit()
except OSError as e:
    print("%s. Please change the port." % e)
    exit()

print("Binding success")

# SQL stuff
# Fetch datatable
show_table_query = "DESCRIBE panda_species"
insert_panda_species = """
INSERT INTO panda_species (name, species, family, population)
Values
    ("Great Panda", "Ailuropoda melanoleuca", "Ursidae", 1527),
    ("Red Fox", "Ailurus fulgens", "Ailuridae", 312)
"""

select_panda_species = "SELECT * FROM panda_species"

# Create table if panda_species does not exist
# Also create rows with some starter data if there are no entries

with mydb.cursor() as cursor:
    try:
        cursor.execute(insert_panda_species)
    except Error:
        print("Creating table panda_species...", end="")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS panda_species(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            species VARCHAR(30),
            family VARCHAR(30),
            population INT
        )
        """)
        cursor.fetchall()
        cursor.execute(insert_panda_species)
        print(" complete!")

    # Print datatable
    cursor.execute(select_panda_species)
    cursor.fetchall()

# Become a server socket and listen for clients
server_socket.listen(5)
print(f"Socket is listening on port {PORT}...")

# Main loop. Keeps the serer running
while True:
    # Accept connections from outside. Program is terminated with CTRL+C
    try:
        client_socket, address = server_socket.accept()
        #print(f"\nReceived connection from {address}", end="\n\n")
    except KeyboardInterrupt:
        print("\nSuccessfully terminated the program.")
        exit()
    except socket.error as msg:
        print("%s" % (msg,))

    # HTTP Requests
    # Receive request from client.
    client_request = client_socket.recv(1024).decode("utf-8")
    request_string = client_request.split(" ")  # Split request from client

    # First element is the request method
    # Second element is the requested file path
    request_method = request_string[0]
    request_file = request_string[1]

    # Split requested file from database queries
    file_name = request_file.split("?")[0]
    file_name = file_name.lstrip("/")
    # Return index.html if no files were requested
    if file_name == "":
        file_name = "index.html"
    # Respond with the requested file. Catch error if file non-existent
    try:
        file = open("%s" % (file_name), 'rb')  # 'rb' = read binary
        response = response = file.read()
        file.close()

        # Create header for server's response to client
        header = "HTTP/1.1 200 OK\n"

        if file_name.endswith(".jpg"):
            mimetype = "image/jpg"
        elif file_name.endswith(".css"):
            mimetype = "text/css"
        else:
            mimetype = "text/html"

        header += "Content-Type: %s\n\n" % mimetype  # + "<strong>\n\n</strong"

    except Exception as e:
        # If page is not found
        header = "HTTP/1.1 404 Not Found \n\n"
        response = "<html>\
                        <body>\
                            <center>\
                            <h3>Error 404: File not found</h3>\
                            <p>Python HTTP Server<p>\
                            </center>\
                        </body>\
                    </html>".encode("utf-8")

    # Respond to client and close socket
    final_response = header.encode("utf-8")
    final_response += response
    client_socket.send(final_response)

    # Close connection
    client_socket.close()

print("Hello")
