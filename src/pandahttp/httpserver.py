"""Create and manage HTTP server

HTTP requests from clients vary and must be handled differently. A request
may be illegal or request a non-existent file. These must be handled accordingly
and properly.

Additionally, also creates and manages HTTP server using the HttpServer class.
The server uses TCP and IPv4 protocols.
"""
from configparser import Error
import socket
import errno
from .terminal import printc
from sys import exit as sysexit


class HttpServer:
    def __init__(self, host: str = "localhost", port: int = 8080, concurrent_clients: int = 5) -> None:
        """HTTP server

        Optionally pass server info to change its behaviour.

        Args:
            host (str, optional): Server hostname. Defaults to "localhost".
            port (int, optional): Server postnumber. Defaults to 8080.
            concurrent_clients (int, optional): Max number of concurrent clients. Defaults to 5.
        """

        # Default server settings
        self.host = host    # IP-address or domain name
        self.port = port    # Port number

        # Amount of clients to listen for before being inavailable
        self.concurrent_clients = concurrent_clients

        # Start server and create socket
        self.server_socket = None

    def create_socket(self, blocking: int = 1, reusable: bool = 0):
        """Create new socket

        Args:
            blocking (int, optional): Whether to set blocking [0/1]. Defaults to 1.
            reusable (bool, optional): Whether to release the socket after closing the server. Defaults to 0.
        """
        try:
            new_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        except Error as e:
            print(e)
            sysexit()

        new_socket.setblocking(blocking)

        # Enable reusing socket after terminating the program.
        # If this is not included, there's a chance that an error will be raised
        # after running the program again on the same socket.
        if reusable:
            new_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.server_socket = new_socket

    def bind_socket(self):
        """Bind socket to host and port
        """

        # Return if the no socket exist
        if self.server_socket is None:
            sysexit("There are no sockets assigned to this object.")

        # Attempt to bind the socket
        try:
            self.server_socket.bind((self.host, self.port))
            printc("Binding socket to host and port success!", "ok")
        except PermissionError as e:
            # Permission denied
            if e.errno == errno.EACCES:
                print(f"{e}. Please ensure that port {self.port} is available.")
                exit()
        except OSError as e:
            # Other unexpected errors
            printc(f"{e}. Please change the port.", "fail")
            sysexit()

    def listen_socket(self):
        """Sets the server to listen to clients
        """
        self.server_socket.listen(self.concurrent_clients)

        # Print message on where the server is listening on
        print(
            f"\nSocket is listening on port {self.port}...\nGo to http://localhost:{self.port} to open website.")

    def loop(self):
        """Main loop

        This function loops indefinitely and handles incoming requests
        """
        while True:
            try:
                client_socket, address = self.server_socket.accept()
            except KeyboardInterrupt:
                printc("\nSuccessfully terminated the program.", "ok")
                exit()
            except socket.error as msg:
                print("%s" % (msg,))
            except Exception as e:
                print(e)
                sysexit()

    def request_handle(request: str) -> str:
        """Processes requests and handle them.

        Process requests and return a HTTP response code and header.

        Args:
            request (str): request string to process

        Returns:
            str: Header returned and to be returned to client.
        """
        pass

    def request_ok() -> str:
        """Received request from client is ok.

        Returns:
            str: Header to be sent back to client.
        """
        pass
