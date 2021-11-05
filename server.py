import socket
from sys import exit

from mysql.connector import connect, Error


# Connect to MySQL database only if login credentials are valid
print("Login to MySQL...")
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
    print("\nSuccessfully logged into database")
    print("Detected unsafe login. Please only use this method for development.")

# Quit program if wrong login credentials
except Error as error:
    print(error)
    exit()

HOST = ""  # Listens to requests coming from the network
PORT = 8000

# Create IPv4 TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("\nSocket successfully created")

# Bind socket to host and port
server_socket.bind((HOST, PORT))

# Become a server socket and listen for clients
server_socket.listen(5)
print(f"Socket is listening on 192.168.1.170 on port {PORT}")

# SQL stuff
# Fetch datatable
show_table_query = "DESCRIBE panda_species"
insert_panda_species = """
INSERT INTO panda_species (species, family, population)
Values
    ("Ailuropoda melanoleuca", "Ursidae", 1527),
    ("Ailurus fulgens", "Ailuridae", 312)
"""

select_panda_species = "SELECT * FROM panda_species"

with mydb.cursor() as cursor:
    cursor.execute(select_panda_species)
    result = cursor.fetchall()

    for row in result:
        print(row)

# Main loop. Keeps the serer running
while True:
    # Accept connections from outside
    client_socket, address = server_socket.accept()
    print(f"Received connection from {address}")

    # Confirm connection
    client_socket.send("Successfully connected to the server".encode())

    # Close connection()
    client_socket.close()
