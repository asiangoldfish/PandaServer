from enum import Enum
from mmap import MAP_SHARED
from sys import exit


class Stderr_Options(Enum):
    JOIN = 1
    PLAIN = 2


class Cli_Parser():
    def __init__(self, arg_dict: dict, arg_string: str, seperator: str, prefix: str, regard_filename: bool = True) -> None:
        """Parses command line arguments and maps them to a prefix of commands. These commands are mapped in a dictionary.

        Args:
            arg_dict(dict):             map of arguments. The key is the argument itself, and value the value to assign the argument.
            arg_string(str):            string of arguments from the command line. Ex. use sys.argv to fetch arguments from the command line.
            seperator(str):             the seperator to split values from keys. Ex. '--port=8080' becomes '--port' and '8080' if the seperator = '='
            prefix(str):                the prefix that every argument should begin with
            regard_filename(bool):      if False, then the parser will consider a given file name as an argument. Set this to True if the file name
                                        has not already been removed.
        """

        self.__arg_dict = arg_dict.copy()
        self.__arg_string = arg_string
        self.__prefix = prefix
        self.__seperator = seperator
        self.__regard_filename = regard_filename

    def get_arg_dict(self):
        return self.__arg_dict

    def join_invalid_args(self, args: str, seperator: str) -> None:
        """Takes a list of strings joins them into a single string

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
        match option:
            case option.JOIN:
                print(
                    f"Invalid argument: {self.join_invalid_args(message, self.__seperator)}")
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
            