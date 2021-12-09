import socket

from sys import exit
import os

# Handles config file
from configparser import ConfigParser

# Enables inputting hidden password
from getpass import getpass

# Custom modules
from pandahttp import terminal, httpserver, mysql


# Open config file, for development use
conf = ConfigParser()
conf.read("settings.ini")

# Clear terminal screen if enabled in config
if conf.get("Default", "clear_terminal") == "true":
    os.system('cls' if os.name == 'nt' else 'clear')

# Host address, port and headersize for messages sent by server
HOST = conf.get("Default", "host")
PORT = int(conf.get("Default", "port"))
HEADERSIZE = int(conf.get("Default", "headersize"))

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
    print(address)
    try:
        client_request = client_socket.recv(1024).decode("utf-8")
    except ConnectionResetError:
        print(f"Closing client: {address}")
        client_socket.close()
        continue

    #terminal.printc(client_request, "warning")
    request_string = client_request.split(" ")  # Split request from client

    # First element is the request method
    # Second element is the requested file path
    try:
        request_method = request_string[0]
        request_file = request_string[1]
    except IndexError:
        print(f"Closing client: {address}")
        client_socket.close()
        continue

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
        print(f"Successfully sent index.html to {address}")

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
    print(f"Closing client: {address}")
    client_socket.close()
