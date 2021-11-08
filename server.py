from logging import WARNING
import socket

from sys import exit
import errno

# Handles config file
from configparser import ConfigParser

from mysql.connector import connect, Error

# Handle urls
from urls import urlpatterns

# Threading for handling client connections more efficiently
import threading

# Handle HTTP requests

# Open config file, for development use
conf = ConfigParser()
conf.read("settings.ini")
# Use the following function to fetch any data from the config file.
# Ex.: conf_get("default", "host")


def conf_get(x, y): return conf.get(x, y)


def printc(string: str, code: str,) -> None:
    """Class for generating strings with colours on terminal. Uses ANSI Escape Codes to generate them.
    A coloured string must be escaped with RESET, otherwise the chosen colour will persist.

    Args:
    -----
        print_string (str): String to print to terminal.

        code (str): Available arguments: OK/Green, WARNING/Yellow, FAIL/Red
    """
    OK = "\033[92m"  # Green
    WARNING = "\033[93m"  # YELLOW
    FAIL = "\033[91m"  # RED
    RESET = "\033[0m"  # RESET COLOUR

    testvar = "OK".casefold

    if code.casefold() == "ok" or code.casefold() == "green":
        colour = OK
    elif code.casefold() == "warning" or code.casefold() == "yellow":
        colour = WARNING
    elif code.casefold() == "fail" or code.casefold() == "red":
        colour = FAIL
    else:
        raise ValueError(
            "Code arg not valid. Check the printc docstring for help.")

    print("%s%s%s" % (colour, (string), RESET))


class SystemCheck:
    """
    Run system check to make sure there are no errors upon running the server. Provides methods to enable
    or disable use of database.
    """

    def __init__(self):
        self.run_system_check()

    def login_db(self) -> None:
        """
        Connect to MYSQL database. 
        """
        # Enables inputting hidden password
        from getpass import getpass

        # Section to fetch in the config file
        section = "Database"

        # Enable auto login for easy testing, debugging or development
        # WARNING: PLEASE DISABLE AUTO LOGIN in the config file before deployment
        try:
            auto_login = conf.getboolean("Database", "auto_login")
        except ValueError as e:
            print(
                f"{e}. Please ensure that the correct value for auto_login is set in the config file.")
            exit()

        # Database login credentials
        # Hard code password for easier time in development. PLEASE DISABLE AUTO LOGIN BEFORE DEPLOYMENT
        if auto_login:
            # The value for these can be changed in the config file
            db_host = conf_get(section, "host")
            db_user = conf_get(section, "user")
            db_pass = conf_get(section, "password")
            db_database = conf_get(section, "database")
        else:
            # Prompt server admin for login credentials to database. SAFE WAY TO RUN THE DB SERVER
            print("Login to MySQL:")
            db_host = input("Host: ")
            db_user = input("Username: ")
            db_pass = getpass("Password: ")
            db_database = input("Database Name: ")

        # Connect to MySQL database only if login credentials are valid
        print("\nLogging into MySQL...")
        try:
            # Temporary solution
            mydb = connect(
                host=db_host,
                user=db_user,
                password=db_pass,
                database=db_database
            )
            printc("\nSuccessfully logged into MYSQL!", "ok")
            # Warn server admin or developer about unsafe login if auto login is enabled.
            if auto_login:
                printc(
                    "\nDetected unsafe login. Auto login is enabled. Please only use this method for development.\n", "warning")

        # Quit program if wrong login credentials
        except Error as error:
            print(error)
            exit()

    def run_system_check(self):
        print("Running system check...")
        if conf.getboolean("Database", "use_db"):
            self.login_db()
        printc("System check complete!", "ok")


syschk = SystemCheck()

# Host address, port and headersize for messages sent by server
HOST = conf_get("Default", "host")
PORT = int(conf_get("Default", "port"))
HEADERSIZE = int(conf_get("Default", "headersize"))

# Create IPv4 TCP socket if permission is there
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enables reuse of socket
old_state = server_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)

printc("Socket successfully created", "ok")

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
        printc("Something went wrong when binding socket to port and host", "fail")
        exit()
except OSError as e:
    printc("%s. Please change the port." % e, "fail")
    exit()

printc("Binding socket to host and port success!", "ok")

# Become a server socket and listen for clients
server_socket.listen(5)
print(
    f"\nSocket is listening on port {PORT}...\nGo to http://localhost:8080 to open website.")

# Main loop. Keeps the serer running
while True:
    # Accept connections from outside. Program is terminated with CTRL+C
    try:
        client_socket, address = server_socket.accept()
        #print(f"\nReceived connection from {address}", end="\n\n")
    except KeyboardInterrupt:
        printc("\nSuccessfully terminated the program.", "ok")
        exit()
    except socket.error as msg:
        print("%s" % (msg,))

    # HTTP Requests
    # Receive request from client.
    client_request = client_socket.recv(1024).decode("utf-8")
    printc(client_request, "warning")
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
