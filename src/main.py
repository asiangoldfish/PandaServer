from sys import stderr
from pandahttp import HttpServer

import json


def main():
    # Get configuration from settings.json
    try:
        with open("settings.json", "r") as file:
            config = file.read().replace("\n", "")
    except FileNotFoundError:
        print("Unable to find the configuration file. It should be named settings.json", file=stderr)
    config = json.loads(config)

    # Server object
    server = HttpServer(
        config["host"],
        int(config["port"]),
        int(config["concurrent_users"])
    )

    server.create_socket(1, True)  # Create new socket
    server.bind_socket()  # Bind socket to host and port
    server.listen_socket()  # Listen for HTTP requests
    server.main_loop()  # Loop forever


if __name__ == "__main__":
    main()
