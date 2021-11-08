"""Create and manage HTTP server

HTTP requests from clients vary and must be handled differently. A request
may be illegal or request a non-existent file. These must be handled accordingly
and properly.

Additionally, also creates and manages HTTP server using the HttpServer class.
The server uses TCP and IPv4 protocols.
"""
import socket
import errno
from .terminal import printc


class HttpServer:

    def __init__(self, host="localhost", port=8080, infinite_connection=True) -> None:
        """Asign required host settings to start the Http server

        Args:
            host (str, optional): [description]. Defaults to "localhost".
            port (int, optional): [description]. Defaults to 8080.
            infinite_connection (bool, optional): [description]. Defaults to True.
        """
        # Default server settings
        self.host = host
        self.port = port
        self.infinite_connection = infinite_connection

        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Enable reusing socket after terminating the program.
        # If this is not included, there's a chance that an error will be raised
        # after running the program again on the same socket.
        self.server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to host (domain/ip) and port
        # Raise error if unsuccessful and terminate the program
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
            exit()

        # Listen to clients
        self.server_socket.listen(5)

        # Print message on where the server is listening on
        if self.host == "":
            # Server is accessible anywhere on the local network
            print(
                f"\nSocket is listening on port {self.port} on the local network...\nGo to http://localhost:8080 to open website.")
        else:
            print(
                f"\nSocket is listening on port {self.port}...\nGo to http://localhost:8080 to open website.")


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
