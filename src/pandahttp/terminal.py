"""Terminal related functionalities.

    Add terminal functionalities beyond what methods such as print offers.
    """


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
