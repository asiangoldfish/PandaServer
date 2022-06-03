"""Manage MySQL database

MySQL is a robust and scalable database server. The PandaHttp MySQL module makes it
easy to implement the server to a project and easily connect the application to
the server.
"""

from mysql.connector import connect, Error
from configparser import ConfigParser
from getpass import getpass  # Secret password
import traceback


class MySql:
    """An all-in-one class for 
     Python to a MySQL database.

    It acts similarly to a macro and all its functionalities derive from
    Oracle's MySQL Connector for Python.
    """

    def login(self, config=None, configsector=None, autologin=None, logincreds=None, logging=True) -> bool:
        """Manage login credentials

        Login may happen either automatically or prompts system admin for credentials.
        If autologin is true, then login credentials must be hardcoded in a way or
        another and passed as arguments. These arguments are passed in as a dictionary.
        Another way is to use a configuration file where all inputs are specified. To
        use this feature, import configparser and pass in an object of class
        ConfigParser.

        Arguments:
        ---
        config (ConfigParser):  Handle entries from configuration file and convert
                                them to variables. The file must include the following
                                entries:

                                auto_login (bool): Whether to auto login with hardcoded
                                                   login credentials.
                                host (str): IPv4 address or domain name of MySQL
                                user (str): MySQL username
                                password (str): MySQL password
                                database (str): MySQL database (can be seen with
                                                'SHOW databases' command)
        configsector (str): The sector in the config file which all MySQL related
                            entries lie under. This is required if config is passed
        autologin (bool): If no config file is specified, then this specifies
                          whether to login MySQL with hardcoded credentials or prompt
                          system administrator.
        logincreds (dict): All login credentials required for MySQL instead of. Please
                           using the config file. Refer to the config argument for a list
                           of all required keys (except auto_login).
        logging (bool): Logs the login process to terminal.

        Returns:
        ---
        (bool): Returns True if login was successful, else returns False
        """

        # Config is None if config as argument hasn't been passed
        if config is not None:
            config = config if config is not None else None
            # Checks that config is instance of ConfigParser. Raise error if not
            if not isinstance(config, ConfigParser):
                raise TypeError("Missing child of class ConfigParser")

            # Configsector: Raise error if config has been passed but not configsector
            # This is used for fetching data from the config file
            if config is not None and configsector is None:
                raise ValueError(
                    "Configsector must be passed as argument to MySql.login")

            # Configsector must be type str for the configparser to work
            if not isinstance(configsector, str):
                raise KeyError("Configsector must be type str")

            # Fetches autologin from config and checks for boolean value
            try:
                # Checks autologin against possible true values...
                if config.get(configsector, "autologin").lower() in ["yes", "1", "true"]:
                    autologin = True
                else:
                    autologin = False
                print(autologin)
            except ValueError:
                raise ValueError(
                    "Autologin for MySQL is not valid. Must be a boolean")
            except KeyError:
                raise KeyError("Key autologging missing in config file")

        # If config file has been passed, aka is not None, then use logincreds instead
        else:
            try:
                # Also checks for dict
                logincreds = dict(logincreds if config is None else None)
            except ValueError:
                raise ValueError(
                    "Login credentials for MySQL are not valid. Must be in a dictionary.")
            except TypeError:
                raise TypeError(
                    "Logincreds must not be 'NoneType' object if config is not used.")

            # Checks that all entries exist in the logincreds dictionary
            if "host" and "user" and "password" and "database" in logincreds:
                pass
            else:
                raise KeyError(
                    "Missing keys in dictionary for MySQL: host, password, and database")

        # MySQL login credentials
        if autologin is True:
            host = config.get(
                configsector, "host") if config is not None else logincreds.get("host")
            user = config.get(
                configsector, "user") if config is not None else logincreds.get("user")
            password = config.get(
                configsector, "password") if config is not None else logincreds.get("password")
            database = config.get(
                configsector, "database") if config is not None else logincreds.get("database")

        # User logs in via terminal if autologin is false
        else:
            try:
                print("Login to MySQL...")
                host = input("Host: ")
                user = input("User: ")
                password = getpass("Password: ")
                database = input("Database: ")
            except KeyboardInterrupt:
                exit("\n")

        # Connect to database
        try:
            mydb = connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )

            print("\nSuccessfully logged into MySQL!")
        except Error as e:
            exit(e)
