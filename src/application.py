from sys import stderr
from sys import exit as sysexit
from pandahttp import HttpServer, printc
from socket import error as socket_error

import json


class Application:
    def __init__(self):
        self.server_socket = None
        self.http_server = None
        self.config = str()

        self.init()

    def init(self):
        # Get configuration from settings.json
        try:
            with open("settings.json", "r") as file:
                json_config = file.read().replace("\n", "")
        except FileNotFoundError:
            print(
                "Unable to find the configuration file. It should be named settings.json",
                file=stderr,
            )
        self.config = json.loads(json_config)

        # Server object
        self.http_server = HttpServer(
            self.config["host"],
            int(self.config["port"]),
            int(self.config["concurrent_users"]),
        )

        self.http_server.create_socket(1, True)  # Create new socket
        self.http_server.bind_socket()  # Bind socket to host and port
        self.http_server.listen_socket()  # Listen for HTTP requests

    def run(self):
        while True:
            try:
                client_socket, address = self.http_server.server_socket.accept()
                # print(f"\nReceived connection from {address}", end="\n\n")

            except KeyboardInterrupt:
                printc("\nSuccessfully terminated the program.", "ok")
                exit()
            except socket_error as msg:
                print("%s" % (msg,))
            except Exception as e:
                print(e)
                sysexit()

            # HTTP Requests
            # Receive request from client.
            # print(address)
            try:
                client_request = client_socket.recv(1024).decode("utf-8")
            except ConnectionResetError:
                print(f"Closing client: {address}")
                client_socket.close()
                continue

            # terminal.printc(client_request, "warning")
            request_string = client_request.split(" ")  # Split request from client

            # First element is the request method
            # Second element is the requested file path
            try:
                request_method = request_string[0]
                request_file = request_string[1]
            except IndexError:
                client_socket.close()
                continue

            # Split requested file from database queries
            file_name = request_file.split("?")[0]
            # Return index.html if no files were requested
            if file_name == "" or file_name == "/":
                # TODO: Write better error handle for developer mistake: key not found
                try:
                    file_name = self.config["default_file"]
                except KeyError:
                    # If page is not found
                    print(
                        f"Configuration in settings.json for 'defaul_fil' does not exist. It is an invalid key."
                    )
                    header = "HTTP/1.1 404 Not Found \n\n"
                    response = "<html>\
                                    <body>\
                                        <center>\
                                        <h3>Error 404: File not found</h3>\
                                        <p>Python HTTP Server<p>\
                                        </center>\
                                    </body>\
                                </html>".encode(
                        "utf-8"
                    )

                    # Respond to client and close socket
                    final_response = header.encode("utf-8")
                    final_response += response
                    client_socket.send(final_response)
                    # printf

                    # Close connection
                    client_socket.close()
                    continue

            else:
                file_name = file_name.lstrip("/")

            # Respond with the requested file. Catch error if file non-existent
            src_dir = self.config["root"]
            try:
                file = open(
                    "%s" % (f"{src_dir}/{file_name}"), "rb"
                )  # 'rb' = read binary
                response = response = file.read()
                file.close()

                # Create header for server's response to client
                header = "HTTP/1.1 200 OK\n"

                # TODO: Find a better way to handle mimetype
                if file_name.endswith(".jpg"):
                    mimetype = "image/jpg"
                elif file_name.endswith(".css"):
                    mimetype = "text/css"
                else:
                    mimetype = "text/html"

                header += "Content-Type: %s\n\n" % mimetype  # + "<strong>\n\n</strong"

            except Exception as e:
                # TODO: Abstract page not found into a separate mechanism or method
                # If page is not found
                header = "HTTP/1.1 404 Not Found \n\n"
                response = "<html>\
                                <body>\
                                    <center>\
                                    <h3>Error 404: File not found</h3>\
                                    <p>Python HTTP Server<p>\
                                    </center>\
                                </body>\
                            </html>".encode(
                    "utf-8"
                )

            # Respond to client and close socket
            final_response = header.encode("utf-8")
            final_response += response
            client_socket.send(final_response)
            # printf

            # Close connection
            client_socket.close()
