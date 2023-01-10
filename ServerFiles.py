import socket
import os

# Set the host and port
HOST = '127.0.0.1'
PORT = 8080

# Create a socket and bind it to the host and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

# Set the socket to listen for incoming connections
server_socket.listen()

# Continuously listen for incoming connections
while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()
    print(f'New connection from {client_address}')

    # Receive the request from the client
    request = client_socket.recv(1024).decode()
    print(f'Received request: {request}')

    # Split the request into the action and file name
    action, file_name = request.split()

    # Check if the request is to view the local files or the server files
    if action == 'LOCAL':
        file_list = ''
        for file in os.listdir():
            file_list += file + '\n'
    elif action == 'SERVER':
        # Get a list of available files on the server
        file_list = ''
        for file in os.listdir(os.getcwd()):
            file_list += file + '\n'
    elif action == 'DOWNLOAD':
        # Check if the file exists
        if os.path.exists(file_name):
            # Open the file in read-binary mode
            with open(file_name, 'rb') as file:
                # Read the contents of the file
                file_contents = file.read()

            # Send the file contents to the client
            client_socket.send(file_contents)
        else:
            # Send an error message to the client
            error_message = 'ERROR: File does not exist'
            client_socket.send(error_message.encode())
    elif action == 'UPLOAD':
        # Receive the file contents from the client
        file_contents = client_socket.recv(1024)

        # Check if the received data is an error message
        if file_contents.startswith('ERROR'.encode()):
            print(file_contents.decode())
        else:
            # Open a new file in write-binary mode
            with open(file_name, 'wb') as file:
                # Write the file contents to the file
                file.write(file_contents)
            print('File uploaded')
    #Close the client socket
    client_socket.close()