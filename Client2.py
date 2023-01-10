import os
import socket

# Configuration constants
HOST = 'localhost'
PORT = 5000
BUFFER_SIZE = 1024

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server
sock.connect((HOST, PORT))

while True:
    # Display the menu
    print('Menu: \n1. View files\n2. Download file\n3. Upload file')
    # Get the user's selection
    choice = input('Enter your choice: ')

    if choice == '1':
        # Send the 'list' command to the server
        sock.send('list'.encode())

        # Receive the list of files from the server
        file_list = sock.recv(BUFFER_SIZE).decode()

        # Split the list of files into a Python list
        file_list = file_list.split()

        # Display the list of files
        print('Files on server:')
        for file in file_list:
            print(file)

        # Ask the user if they want to see local files
        view_local = input('View local files? (y/n) ')
        if view_local == 'y':
            # Get a list of local files
            local_files = os.listdir()
            print('Files on local:')
            for file in local_files:
                print(file)
    elif choice == '2':
        # Ask the user for the file they want to download
        file_name = input('Enter the file to download: ')

        # Send the 'download' command and the file name to the server
        sock.send(f'download {file_name}'.encode())

        # Receive the file from the server
        with open(file_name, 'wb') as file:
            chunk = sock.recv(BUFFER_SIZE)
            while chunk:
                file.write(chunk)
                chunk = sock.recv(BUFFER_SIZE)
        print(f'File {file_name} downloaded')
    elif choice == '3':
        # Ask the user for the file they want to upload
        file_name = input('Enter the file to upload: ')

        # Check if the file exists
        if not os.path.exists(file_name):
            print(f'Error: File {file_name} does not exist')
            continue

        # Send the 'upload' command and the file name to the server
        sock.send(f'upload {file_name}'.encode())

        # Open the file for reading
        with open(file_name, 'rb') as file:
            # Read the file in chunks and send each chunk to the server
            chunk = file.read(BUFFER_SIZE)
            while chunk:
                sock.send(chunk)
                chunk = file.read(BUFFER_SIZE)
        print(f'File {file_name} uploaded')

    sock.close()
