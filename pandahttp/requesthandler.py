"""Create headers for HTTP requests.

HTTP requests from clients vary and must be handled differently. A request
may be illegal or request a non-existent file. These must be handled accordingly
and properly.
"""


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
