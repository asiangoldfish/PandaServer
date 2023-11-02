# **Panda Server**

**WARNING!** *DO NOT* use this server for production or expose it to the public!! This server is vulnerable and *will* expose your system to exploits and serious damage. Use this server only on your local network and local machine.

## **Links**
- [What is Panda Server](#what-is-panda-server)
- [Run your own Panda Server](#run-your-own-pandaserver)
- [Configuration](#configuration)
- [Useful Resources](#useful-resources)

## What Is Panda Server
Panda Server is a HTTP server and a learning tool to understand how the TCP/IP model works at the application layer. It's written primarily with novice penetration testers in mind and developers that wish to understand how a web server works. It will never be as secure, maintained and usable as popular software like Nginx or Apache, and neither is it intended to be so.

With that out of the way, what exactly is this all about? Panda Server is purely written with Python 3 and serves as a simple web server. It supports MySQL and MariaDB databases and is also well documented. Although the server is highly configurable, the project comes with default configuration values and works right out of the box.

The project relies heavily on Python's builtin socket module and greatly attempts to maintain a clean and organized project and code structure. With this, it aims to encourage new programmers to checkout well-documented code without being overwhelmed. Furthermore, it serves as an example on how the socket module can be used and integrated with other modules. Panda Server comes with a custom module named "pandahttp" where codes for handling HTTP requests and managing databases reside.

This is a personal project. As the server is not intended for production, but merely a simple development software for front-end development, the software will have limitations. This is especially true with security, as it does not run all the necessary checks to protect the system against attacks like SQL injections, cross-site scripting (XSS), local file inclusion attacks (LFI), reverse shell and other serious attacks. This can make the software a practise target to penetration testers.

## Run your own PandaServer
The project is developed with Debian 11, but should work on any other Linux distributions. Some features in the future may not work on Windows, but this will eventually be documented as the project is developed. The project also includes live reload feauture. This requires NodeJS. That said, let's get started.

- The project includes a utility command `panda-manager`. This helps with managing the project, its dependencies and additional utilities. It is still recommended to install all dependencies on beforehand to avoid confusions.
- Install the following packages: curl, git, python3, python3-pip, python3-venv, nodejs, nodemon
```
sudo apt update
sudo apt install curl git python3 python3-pip python3-venv nodejs
```
- Clone the repository
    ```
    git clone https://github.com/asiangoldfish/PandaServer.git
    cd PandaServer/
    ```

- Create and activate virtual environment
    ```
    python -m venv venv
    source venv/bin/activate
    ```

- Start the server
    ```
    python3 src/main.py
    ```

---

## Configuration
Configuration is performed in [settings.json](settings.json). Note: Any other configurations are currently not in use or
in development.

| name | default value | description |
|:-----|:--------------|:------------|
| host | localhost | The hostname or IP address that the user can connect to the server with |
| port | 8080 | Port number to open an expose the web engine to |
| clear_terminal | false | Clear the terminal before starting the server. This hides previously printed outputs |
| root | /opt/PandaServer/templates | Default location for static files |
| default_file | index.html | If the user does not provide files in the URI, eg. _http://localhost:8080/_, the default file will be served. |

## Useful Resources
- Handling HTTP requests: [Stack Overflow](https://stackoverflow.com/questions/41386086/handling-client-requests-in-http-server)