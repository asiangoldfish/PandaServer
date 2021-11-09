import socket

from sys import exit
import errno

# Handles config file
from configparser import ConfigParser

# Enables inputting hidden password
from getpass import getpass

# Custom modules
from pandahttp import terminal, httpserver

# Open config file, for development use
conf = ConfigParser()
conf.read("settings.ini")
# Use the following function to fetch any data from the config file.
# Ex.: conf_get("default", "host")


def conf_get(x, y): return conf.get(x, y)


class SystemCheck:
    """
    Run system check to make sure there are no errors upon running the server. Provides methods to enable
    or disable use of database.
    """

    def __init__(self):
        pass

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
            terminal.printc("\nSuccessfully logged into MYSQL!", "ok")
            # Warn server admin or developer about unsafe login if auto login is enabled.
            if auto_login:
                terminal.printc(
                    "\nDetected unsafe login. Auto login is enabled. Please only use this method for development.\n", "warning")

        # Quit program if wrong login credentials
        except Error as error:
            print(error)
            exit()

    def run_system_check(self):
        print("Running system check...")
        if conf.getboolean("Database", "use_db"):
            self.login_db()
        terminal.printc("System check complete!", "ok")


syschk = SystemCheck()
syschk.run_system_check()

# Host address, port and headersize for messages sent by server
HOST = conf_get("Default", "host")
PORT = int(conf_get("Default", "port"))
HEADERSIZE = int(conf_get("Default", "headersize"))

# Create socket and bind it to host
server = httpserver.HttpServer(HOST, PORT)

# Main loop. Keeps the server running
while True:
    # Accept connections from outside. Program is terminated with CTRL+C
    try:
        client_socket, address = server.server_socket.accept()
        #print(f"\nReceived connection from {address}", end="\n\n")
    except KeyboardInterrupt:
        terminal.printc("\nSuccessfully terminated the program.", "ok")
        exit()
    except socket.error as msg:
        print("%s" % (msg,))

    # HTTP Requests
    # Receive request from client.
    client_request = client_socket.recv(1024).decode("utf-8")
    terminal.printc(client_request, "warning")
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
