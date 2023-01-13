# Group 11 - Suus Plaum, Oscar Lodeizen, Julius Jorna, Milan Sonneveld, Rogier Wijnants
import time
import socket
import pickle

HEADER = 64
PORT = 2888
FORMAT = 'utf-8'
BUFFER_SIZE = 1024
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
t=0

def start():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(msg, client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    backmsg = (client.recv(2048).decode(FORMAT))
    print(backmsg)

    return backmsg

#Specification 2 allow user to log in with credentials
def checkpassword(chosenoption):

    if chosenoption == str(0):
        username = input("Enter your desired username here: ")
        password = input("Enter your desired password here: ")
        return f"{username}.!{password}.!{chosenoption}"

    elif chosenoption == str(1):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        return f"{username}.!{password}.!{chosenoption}"

    # Check if the entered username and password match any of the sets of credentials
client = start()
while True:

    if t==0:

        send('hello server I would like to make contact',client)
        chosenoption = input('')
        returnmsg = send(checkpassword(chosenoption), client)
        if returnmsg == 'invalid credentials':
            t = 0
            continue
        else:
            t=1
    elif t==1:
        backmsg = (client.recv(2048).decode(FORMAT))
        print(backmsg)

        while True:

            l = input('')
            t = send(l, client)
            if 'invalid' in t:
                backmsg = (client.recv(2048).decode(FORMAT))
                print(backmsg)
            if l == 3:
                filename = input('')
                send(filename, client)
                with open(filename, 'wb') as f:
                    while True:
                        data = client.recv(1024)
                        if not data:
                            break
                        f.write(data)
                    print(f'File {filename} downloaded')

            elif l == 2:
                file_name = input('')
            # Send the file name to the server
                send(file_name, client)

            # Open the file
                with open(file_name, "rb") as f:
                # Read and send the file data
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        client.sendall(data)

            elif l == 4:
                file = input('')
                file_list = send(file, client)

                # Split the list of files into a Python list
                file_list = file_list.split()
                # Display the list of files
                print('Files:')
                for file in file_list:
                    print(file)
                time.sleep(5)
                send('received files', client)

client.close()
