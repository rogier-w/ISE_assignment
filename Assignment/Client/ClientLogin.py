import os
import time
import socket
from pathlib import Path
HEADER = 64
PORT = 6000
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

def readfile(filename):
    txt = Path(filename).read_text()
    return txt
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


            elif l == '2':

                file_name = input('')
                send(file_name, client)

                # Read the file in chunks and send each chunk to the server
                filedata = readfile(file_name)
                print(f'File {file_name} uploaded')

                send(filedata, client)
                time.sleep(2)
            elif l == '3':

                filename1 = input('')
                filedata = send(filename1, client)
                with open(filename1, 'w') as file:
                    file.write(filedata)
                send(filedata, client)
                time.sleep(2)


            elif l == '4':
                file = input('')
                if file  =='2':
                    file_list = ''
                    print('Files:')
                    for file in os.listdir(os.getcwd()):
                        print(file)
                    time.sleep(5)
                    send('received files', client)
                elif file == '1':

                    file_list = send(file, client)
                    time.sleep(5)
                    backmsg = (client.recv(2048).decode(FORMAT))
                    print(backmsg)


                # Split the list of files into a Python list
                file_list = file_list.split()
                # Display the list of files






client.close()
