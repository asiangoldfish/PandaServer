from sys import argv
from pandahttp import HttpServer
from utils.cli_parser import Cli_Parser


def main(argc: int, argv: str):
    """Server main function

    This is the server's starting function.

    Args:
        argc (int): number of arguments passed to this script
        argv (str): string of arguments passed to this script
    """

    # These are the args that this script will accept. Example: "--port=8080"
    options = {
        "--host": str(),
        "--port": int(),
        "--concurrent_clients": 1,
    }

    # This object parses command-line arguments
    parser = Cli_Parser(
        arg_dict=options,       # Accepted arguments
        arg_string=argv,        # String of all arguments
        seperator='=',          # Key-value delimiter
        prefix="--",            # Option prefix
        regard_filename=False,  # Whether to ignore this script's filename
    )

    parser.validate_args()      # Ensure that all arguments are valid

    # Server object
    server = HttpServer(
        host=parser.get_arg_dict()["--host"],       # Hostname
        port=int(parser.get_arg_dict()["--port"]),  # Port number
        # Number of concurrent clients
        concurrent_clients=int(parser.get_arg_dict()["--concurrent_clients"])
    )

    server.create_socket(1, True)   # Create new socket
    server.bind_socket()            # Bind socket to host and port
    server.listen_socket()          # Listen for HTTP requests
    server.loop()                   # Loop forever

if __name__ == "__main__":
    main(len(argv), argv)
