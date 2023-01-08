import socket
import os
# Set the host and port
HOST = '127.0.0.1'
PORT = 8080

# Create a socket and connect to the host and port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Continuously get user input and send requests to the server
while True:
    # Print the menu
    print("Menu:\n1 -  View files\n2 - Download\n3 - Upload\n4 - Chat\n5 - Logout")


    # Get the user's choice
    choice = int(input('Enter a number: '))
    while not (choice >= 1 and choice <= 5):
        choice = int(input("Enter a number: "))

    # Check if the choice is to view the local files
    # Check if the choice is to view the server files
    if choice == 1:
        print("Location of the files?: \n1 - Local\n2 - Server: ")
        file_location = int(input("Enter a number: "))
        while not (choice >= 1 and choice <= 2):
            file_location = int(input("Enter a number: "))
        if file_location == 1:
            request = 'LOCAL'
        elif file_location == 2:
            request = 'SERVER'

    # Check if the choice is to download a file
    elif choice == 2:
        file_name = input('Enter a file name: ')
        request = 'DOWNLOAD ' + file_name
    # Check if the choice is to upload a file
    elif choice == 3:
        file_name = input('Enter a file name: ')
        # Check if the file exists
        if os.path.exists(file_name):
            # Open the file in read-binary mode
            with open(file_name, 'rb') as file:
                # Read the contents of the file
                file_contents = file.read()

            # Send the request and file contents to the server
            request = 'UPLOAD ' + file_name
            client_socket.send(request.encode())
            client_socket.send(file_contents)
        else:
            # Send an error message to the server
            error_message = 'ERROR: File does not exist'
            client_socket.send(error_message.encode())
            continue
    else:
        # Send an error message to the server
        error_message = 'ERROR: Invalid choice'
        client_socket.send(error_message.encode())
        continue



    # Send the request to the server
    client_socket.send(request.encode())

    # Receive the response from the server
    response = client_socket.recv(1024).decode()
    print(response)

    # Check if the received data is an error message
    if response.startswith('ERROR'):
        print(response)
    else:
        # Split the response into the action and file list
        action, file_list = response.split('\n', 1)

        # Print the list of available files
        print(file_list)

        # Check if the action is to download a file
        if action == 'DOWNLOAD':
            # Open a new file in write-binary mode
            with open(file_name, 'wb') as file:
                # Write the file contents to the file
                file.write(response)
            print('File downloaded')

# Close the client socket
    client_socket.close()