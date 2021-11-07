from os import error, system
from settings import server_script
import sys

# Check if this script is running in a virtual environment
def check_venv() -> bool:
    """
    Call this function to check if this script is run within a virtual environment or not.

    Returns:
        bool: Returns True if within a virtual environment, or False if not.
    """
    def get_base_prefix_compat():
        """Get base/real prefix, or sys.prefix if there is none."""
        return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

    def in_virtualenv():
        return get_base_prefix_compat() != sys.prefix

    return in_virtualenv()


def commands():
    print("""Execute commands with python3 manage.py <subcommand>.

commands - List all available arguments for manage.py
help - More to come
runserver - Run the server. Currently only runs on port 8080
""")


def help():
    print("You have asked for help, but I have no help to give you :(")


def runserver():
    system("python3 server.py")
    """try:
        system("ls %s | entr python3 manage.py runserver" % (server_script,))
    except error:
        print(error)"""


def main():
    """Main function of the program"""

    list_of_commands = [
        "commands",
        "help",
        "runserver",
    ]
    
    # Allow only one argument
    if len(sys.argv) > 2:
        return "Too many arguments. Terminating the program."
        
    if len(sys.argv) <= 1:
        commands()
        exit()

    # Check for arguments and execute them accordingly
    if sys.argv[1] not in list_of_commands:
        print("No commands were found.")
    else:
        # Find commands based on a dictionary with keys for each command
        switcher = {
            "help": help,
            "commands": commands,
            "runserver": runserver,
        }
        key = sys.argv[1]
        default = ""
        value = switcher.get(key, default)

        # Execute command. Raise error if the command is not in the dictionary
        try:
            value()
        except TypeError:
            print('Missing entry "%s" in the switcher dictionary.' % (key,))


if __name__ == "__main__":
    main()
