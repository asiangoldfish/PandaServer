# **Panda Server**

**WARNING!** Please do not use this server for production or expose it to the world wide web!! This is an extremely insecure and vulnerable server and *will* expose your computer to exploits. Use this server at your own risk.

Panda Server is an HTTP server project and can be used as a learning tool to understand how the TCP/IP model works at the application layer. It's written by somebody who is learning Python and the essence of how the TCP/IP model, networking and servers work. It can additionally be used as a practise target for exploitations.

---

## **Links**
- [Test your own Panda Server](#test-your-own-pandaserver)

## **Run your own PandaServer**
The project is developed with Debian 11, but should work on any other Linux distributions. Some features in the future may not work on Windows, but this will eventually be documented as the project is developed. That said, let's get started.

- This project uses Python 3. Python versions earlier than 3.6 may or may not work. Install Python 3 with `sudo apt install python3` or go to https://python.org/downloads.

- Create a virtual environment with `python3 -m venv venv`.

- If you don't already have pip installed, install it with `sudo apt install python3-pip`.

- Install all dependencies with `pip3 install -r requirements.txt`.

- At the moment the main script is `server.py`. Run this script with `python3 server.py`.

Happy hacking! :)