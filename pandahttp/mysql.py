"""Manage MySQL database

MySQL is a robust and scalable database server. The PandaHttp MySQL module makes it
easy to implement the server to a project and easily connect the application to
the server.
"""

from mysql.connector import connect
from configparser import ConfigParser
from getpass import getpass  # Secret password


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
                            entries lie under.
        autologin (bool): If no config file is specified, then this specifies
                          whether to login MySQL with hardcoded credentials or prompt
                          system administrator.
        logincreds (dict): All login credentials required for MySQL. Please refer to
                           the config argument for a list of all required keys (except
                           auto_login).
        logging (bool): Logs the login process to terminal.

        Returns:
        ---
        (bool): Returns True if login was successful, else returns False
        """

        # Check for NoneType
        config = config if config is not None else None
        # Checks that config is instance of ConfigParser. Raise error if not
        if not isinstance(config, ConfigParser):
            raise ValueError("Missing child of class ConfigParser")

        configsector = configsector if config is not None else None
        try:
            # Also checks for bool
            autologin = bool(autologin if config is None else config.get(
                configsector, "autologin"))
        except ValueError:
            exit("Autologin for MySQL is not valid. Must be a boolean")
        except KeyError:
            exit("Key autologging missing in config file")

        try:
            # Also checks for dict
            logincreds = dict(logincreds if config is None else None)
        except ValueError:
            exit("Login credentials for MySQL are not valid. Must be in a dictionary.")

        # Checks that all entries exist in the logincreds dictionary
        if "host" and "password" and "database" in logincreds:
            pass
        else:
            exit("Missing keys in dictionary for MySQL: host, password, and database")

        # Assign vars for login credentials
        host = config.get(
            configsector, "host") if config is not None else logincreds.get()
        #password = confi
