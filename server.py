import socket

from sys import exit
import errno
import os

from mysql.connector import connect, Error


# Connect to MySQL database only if login credentials are valid
print("Running system checks...")
print("Logging into MySQL...")
try:
    # Bug: Server closes and can't be opened again
    """
    with connect(
        host="localhost",
        user="test_user",
        password="test_user123",
        database="panda",
    ) as mydb:
        print("\nSuccessfully logged into database")
        print("Detected unsafe login. Please only use this method for development.")
    """
    # Temporary solution
    mydb = connect(
        host="localhost",
        user="test_user",
        password="test_user123",
        database="panda",
    )
    print("\nSuccessfully logged into MYSQL!")
    print("Detected unsafe login. Please only use this method for development.")

# Quit program if wrong login credentials
except Error as error:
    print(error)
    exit()

print("\nSystem checks complete!")

HOST = ""  # Listens to requests coming from the network
PORT = 8000

# Create IPv4 TCP socket if permission is there
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("\nSocket successfully created")

# Bind socket to host and port
try:
    server_socket.bind((HOST, PORT))
except PermissionError as e:
    # Permission denied
    if e.errno == errno.EACCES:
        print("%s most likely due to port number %i" % (e.strerror, PORT))
        exit()
    else:
        print("Something went wrong when binding socket to port and host")
        exit()

print("Binding success")

# SQL stuff
# Fetch datatable
show_table_query = "DESCRIBE panda_species"
insert_panda_species = """
INSERT INTO panda_species (name, species, family, population)
Values
    ("Great Panda", "Ailuropoda melanoleuca", "Ursidae", 1527),
    ("Red Fox", "Ailurus fulgens", "Ailuridae", 312)
"""

select_panda_species = "SELECT * FROM panda_species"

# Create table if panda_species does not exist
# Also create rows with some starter data if there are no entries

with mydb.cursor() as cursor:
    try:
        cursor.execute(insert_panda_species)
    except Error:
        print("Creating table panda_species...", end="")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS panda_species(
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(30) NOT NULL,
            species VARCHAR(30),
            family VARCHAR(30),
            population INT
        )
        """)
        cursor.fetchall()
        cursor.execute(insert_panda_species)
        print(" complete!")
    
    # Print datatable
    cursor.execute(select_panda_species)
    cursor.fetchall()

# Become a server socket and listen for clients
server_socket.listen(5)
print(f"Socket is listening on port {PORT}...")

# Main loop. Keeps the serer running
while True:
    # Accept connections from outside. Program is terminated with CTRL+C
    try:
        client_socket, address = server_socket.accept()
        print(f"Received connection from {address}")
    except KeyboardInterrupt:
        print("\nSuccessfully exit the program.")
        exit()

    # Confirm connection
    client_socket.send("Successfully connected to the server".encode())

    # Close connection()
    client_socket.close()
