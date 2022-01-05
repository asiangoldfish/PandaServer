# List of Commands Not Found
The panda-manager script internally executes Bash commands and relies on already available commands to the current user. If these commands are not found, then the script will mention the specific command it tried to execute. In this page, you will find a detailed overview over all possible commands that may occur and how to fix the issues.

The format of the error looks like this:
```
Error 2: Command [command] not found."
```

List of commands:
- [Python3](#python3)
- [Browser](#browser)
- [Nodemon](#nodemon)
- [Curl](#curl)
- [Pip3](#pip3)

## Python3
The Panda Server is written with Python version 3. The script attempts to use the command `python3` to launch the server. If this command is unavailable, then the process fails. Make sure that Python version 3 is installed before continuing.

## Browser
After using the option -b or --browser, the script expects a browser to be passed. If the command for launching the browser is invalid, the program terminates. Ensure that the command for opening the chosen browser is correct on your operating system.

## Nodemon
Nodemon is a NodeJS application that watches files for any changes. Upon saving a change, Nodemon will restart a script automatically. This is especially useful for development. Panda Server requires this module if live reload is enabled. To install Nodemon, follow these steps:
1. Install NodeJS. The process varies depending on the operating system.
2. Make sure that Node's Package Manager (npm) is installed. This is usually installed automatically with NodeJS.
3. Use the following command:
    ```
    node i -g nodemon
    ```
    Note that this will install nodemon globally. This is required for the Panda Server for the live reload feature to work.

## Curl
Curl is a popular tool for fetching data from webservers using HTTP requests. Panda-manager requires this to download files from the project's remote repository at GitHub. The installation process varies depending on the operating system, but most Linux distributions' repositories come with this tool preinstalled.

## Pip3
Pip is Python's package manager. The project uses this to install and manage dependencies. It usually comes installed with Python, although this varies depending on the operating system.