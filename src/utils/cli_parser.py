from enum import Enum
from sys import exit


class Stderr_Options(Enum):
    JOIN = 1
    PLAIN = 2


class Cli_Parser():
    def __init__(self, arg_dict: dict,
                 arg_string: str,
                 seperator: str,
                 prefix: str,
                 regard_filename: bool = True
                 ) -> None:
        """Parses command line arguments and maps them to a prefix of commands.
        These commands are mapped in a dictionary.

        Args:
            arg_dict(dict):             all valid arguments and default values
            arg_string(str):            script args from the cli
            seperator(str):             the seperator to split values from keys
            prefix(str):                argument prefix
            regard_filename(bool):      whether to consider script name in args
        """

        self.__arg_dict = arg_dict.copy()   # Valid possible arguments
        self.__arg_string = arg_string      # CLI-arguments to parse
        self.__prefix = prefix              # Characters to signify an option
        self.__seperator = seperator        # Argument character delimiter
        # Whether to consider script name in argstring
        self.__regard_filename = regard_filename

    def get_arg_dict(self):
        """Gets the dictionary stored in a Cli_parser object

        Use this function to return the dictionary with stored argument values.

        Example:
            Get hostname: parser.get_arg_dict()["--host"]

        Returns:
            dict: Data structure where arguments' values are stored
        """
        return self.__arg_dict

    def _join_args(self, args: str, seperator: str) -> str:
        """Take a list of arguments joins them into a single string

        Args:
            args(str): List of arguments
            seperator(str): The seperator that splits the arguments
        """

        out_str = str()

        for i, arg in enumerate(args):
            out_str = f"{out_str}{arg}"

            if i + 1 < len(args):
                out_str = f"{out_str}{seperator}"

        return out_str

    def print_stderr(self, message: str, option: Stderr_Options):
        """Print error message

        Args:
            message (str): Error message to print
            option (Stderr_Options): JOIN is the argument contains a delimiter,
                                     PLAIN if not.
        """
        match option:
            case option.JOIN:
                print(
                    f"Invalid argument: {self._join_args(message, self.__seperator)}")
            case option.PLAIN:

                print(f"Invalid argument: {message}")

    def map_args(self, keypair) -> None:
        """Maps an arbitrary list of string-pair to a dictionary.

        Args:
            keypair (str): list of key and value that is mapped to the dictionary
        """
        self.__arg_dict[keypair[0]] = keypair[1]

    def validate_args(self) -> None:
        """Validate command line arguments. Output stderr if an argument is invalid.

        This method also changes the values of the arg_dict that was used as input
        """

        # makes a duplicate of __arg_dict to prevent mutating arg_dict from outside this object
        if not self.__regard_filename:
            # disregard the file name as argument if enabled
            self.__arg_string.pop(0)

        for keyword in self.__arg_string:
            # splits the argument by '='
            keyword = keyword.split(self.__seperator)

            # if an argument with more than 2 elements is found, then print error msg to stdout
            # or raise an error if an argument doesn't start with "--"
            # or raise an error if the argument doesn't exist in the dictionary
            if len(keyword) != 2 or keyword[0][:2] != self.__prefix or not keyword[0] in self.__arg_dict:
                self.print_stderr(keyword, Stderr_Options.JOIN)
                exit()

            # assign command line arguments to fields in the Http_Options struct
            self.map_args(keyword)
