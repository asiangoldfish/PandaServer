from sys import argv
from pandahttp import HttpServer
from utils.cli_parser import Cli_Parser


def main(argc: int, argv: str):

    # Keys that will be considered as commmand line arguments
    options = {
        "--host": str(),
        "--port": int,
        "--concurrent_clients": 1,
    }

    parser = Cli_Parser(
        arg_dict=options,
        arg_string=argv,
        seperator='=',
        prefix="--",
        regard_filename=False,
    )

    parser.validate_args()

    server = HttpServer(
        host=parser.get_arg_dict()["--host"],
        port=int(parser.get_arg_dict()["--port"]),
        concurrent_clients=int(parser.get_arg_dict()["--concurrent_clients"])
    )

    server.create_socket(1, True)
    server.bind_socket()
    server.listen_socket()
    server.loop()

if __name__ == "__main__":
    main(len(argv), argv)
