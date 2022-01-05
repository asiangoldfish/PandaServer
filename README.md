# **Panda Server**

**WARNING!** *DO NOT* use this server for production or expose it to the public!! This server is vulnerable and *will* expose your system to exploits and serious damage. Use this server only at your local network and on your local machine.

Panda Server is a HTTP server and a learning tool to understand how the TCP/IP model works at the application layer. It's written primarily for novice penetration testers in mind and for developers that wish to understand how web servers actually work. It will never be as secure, maintained and usable as popular software like Nginx or Apache, and is neither intended to be so.

---

## **Links**
- [What is Panda Server](#what-is-panda-server)
- [Run your own Panda Server](#run-your-own-pandaserver)
- [How it works](#how-it-works)
- [Error Codes](/docs/errors.md)
- [Useful Resources](#useful-resources)

---

## What Is Panda Server


## Run your own PandaServer
The project is developed with Debian 11, but should work on any other Linux distributions. Some features in the future may not work on Windows, but this will eventually be documented as the project is developed. That said, let's get started.

- This project uses Python 3. Python versions earlier than 3.6 may or may not work. Install Python 3 with `sudo apt install python3` or go to https://python.org/downloads.
- Download the repository with git. Install git with `sudo apt install git` if you don't already have it, then clone the project: `git clone https://github.com/asiangoldfish/PandaServer.git`
- Change to the PandaServer directory with `cd PandaServer`
- Create a virtual environment with `python3 -m venv venv`. All dependencies will be installed here.
- If you don't already have pip installed, install it with `sudo apt install python3-pip`.
- Activate the virtual environment with `source venv/bin/activate`
- Install all dependencies with `pip3 install -r requirements.txt`.
- At the moment the main script is `server.py`. Run this script with `python3 server.py`.

Happy hacking! :)

---

## How it works

The core of the server is the socket module. This module takes care of the networking part. By default, the project is configured to utilize the TCP protocol with IPv4. Host address is configured in the settings.ini file under the "Default" section. Port number is also configured here. A socket is then created and bound to the host and and port, and then is set to listen for clients. In the main script (/server.py), the magic happens inside the while loop. If there are more while loops, then it's the first loop that is responsible for keeping the server running indefinitely.

The logic for handling HTTP requests and managing the server security is written manually. This is why the server is insecure.

As the project is developed, vulnerabilities are slowly patched, new features are implemented, new bugs are introduced and eventually are fixed. If you'd like to practise on your exploitation skills, feel free to download or clone the project and go ham with it.

I strongly recommend to run this project in a virtual machine so you don't accidentally screw your computer up if you choose to use it as a practise target.

## Useful Resources
- Handling HTTP requests: [Stack Overflow](https://stackoverflow.com/questions/41386086/handling-client-requests-in-http-server)