import os
import socket

# Configuration constants
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
sock.bind((HOST, PORT))

# Set the socket to listen for incoming connections
sock.listen(1)

while True:
    # Wait for a client to connect
    print('Waiting for a client to connect...')
    connection, client_address = sock.accept()
    print(f'Client {client_address} connected')

    # Receive the request from the client
    request = connection.recv(BUFFER_SIZE).decode()
    print(f'Received request: {request}')

    # Split the request into the command and the file name
    command, file_name = request.split()

    # Check if the command is 'list'
    if command == 'list':
        # Get a list of files in the current directory
        file_list = os.listdir()

        # Send the list of files to the client
        connection.send(' '.join(file_list).encode())
    # Check if the command is 'download'
    elif command == 'download':
        # Check if the file exists
        if not os.path.exists(file_name):
            # Send an error message to the client
            connection.send('Error: File does not exist'.encode())
        else:
            # Open the file for reading
            with open(file_name, 'rb') as file:
                # Read the file in chunks and send each chunk to the client
                chunk = file.read(BUFFER_SIZE)
                while chunk:
                    connection.send(chunk)
                    chunk = file.read(BUFFER_SIZE)

    # Check if the command is 'upload'
    elif command == 'upload':
        # Open the file for writing
        with open(file_name, 'wb') as file:
            # Receive the file in chunks and write each chunk to the file
            chunk = connection.recv(BUFFER_SIZE)
            while chunk:
                file.write(chunk)
                chunk = connection.recv(BUFFER_SIZE)

    connection.close()
    print(f'Connection to {client_address} closed')
