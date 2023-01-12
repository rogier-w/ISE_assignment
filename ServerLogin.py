import os
import socket
import threading
import time
import hashlib
from datetime import datetime
from pathlib import Path

HEADER = 64
BUFFER_SIZE = 1024
PORT = 6000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
serverudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    login(conn)

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:

            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            msgback = 'received message'
            if '.!' in msg:
                print('hi')
                msgback, username = checkuserandpass(msg)
                conn.send(msgback.encode(FORMAT))
                if msgback == 'successfully logged in' or msgback == 'account made':
                    print('worked')
                else:
                    continue

            while True:
                conn.send('''Please select an option:
                1 - chat
                2 - upload file
                3 - download files
                4 - view files'''.encode(FORMAT))
                msg_length1 = conn.recv(HEADER).decode(FORMAT)
                if msg_length1:

                    msg_length1 = int(msg_length1)
                    msg1 = conn.recv(msg_length1).decode(FORMAT)
                    print(f"[{addr}] {msg1}")
                    print(type(msg1))
                    if '1' == msg1:
                        chat = readchat()

                        conn.send(chat.encode(FORMAT))
                        msg_length2 = conn.recv(HEADER).decode(FORMAT)
                        msg_length2 = int(msg_length2)
                        msg = conn.recv(msg_length2).decode(FORMAT)
                        print(f"[{addr}] {msg}")
                        writetochatlog(username, msg)
                    elif '2' == msg1:
                        conn.send('Please enter a filename: '.encode())
                        filename = conn.recv(2048).decode(FORMAT)
                        with open(filename, 'wb') as file:
                            # Receive the file in chunks and write each chunk to the file
                            chunk = conn.recv(BUFFER_SIZE)
                            while chunk:
                                file.write(chunk)
                                chunk = conn.recv(BUFFER_SIZE)

                    elif '3' == msg1:
                        conn.send('Please enter a filename: '.encode())
                        filename = conn.recv(2048).decode(FORMAT)
                        if not os.path.exists(filename):
                            # Send an error message to the client
                            conn.send('Error: File does not exist'.encode())
                        else:
                            # Open the file for reading
                            with open(filename, 'rb') as file:
                                # Read the file in chunks and send each chunk to the client
                                chunk = file.read(BUFFER_SIZE)
                                while chunk:
                                    conn.send(chunk)
                                    chunk = file.read(BUFFER_SIZE)

                    elif '4' == msg1:
                        conn.send('Do you want to view server files or local files?\n1 - Server\n2 - Local'.encode(FORMAT))
                        msg_length3 = conn.recv(HEADER).decode(FORMAT)
                        msg_length3 = int(msg_length3)
                        msg = conn.recv(msg_length3).decode(FORMAT)
                        if msg == '1':
                            filelist = ''
                            for file in os.listdir(os.getcwd()):
                                filelist += file + '\n'
                                conn.send(' '.join(filelist).encode())
                        if msg == '2':
                            file_list = ''
                            for file in os.listdir():
                                file_list += file + '\n'
                                conn.send(' '.join(file_list).encode())
                    elif msgback == DISCONNECT_MESSAGE:
                        connected = False
                        conn.close()
                    else:
                        conn.send('invalid choice try again \n'.encode(FORMAT))


def login(conn):
    conn.send("""please login to continue, if you already have an account press 1 if you want to make a new account press 0 """
              .encode(FORMAT))

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("\n")
        print(f"[ACTIVE CONNECTION] {threading.active_count() - 1}")

#def uploadfiles():
    # Open the file for writing
    #with open(filename, 'wb') as file:
        # Receive the file in chunks and write each chunk to the file
        #chunk = conn.recv(BUFFER_SIZE)
       # while chunk:
            #file.write(chunk)
            #chunk = conn.recv(BUFFER_SIZE)

#def downloadfiles(filename):
    # Check if the file exists
    #if not os.path.exists(filename):
        # Send an error message to the client
        #conn.send('Error: File does not exist'.encode())
    #else:
        # Open the file for reading
        #with open(filename, 'rb') as file:
            # Read the file in chunks and send each chunk to the client
           # chunk = file.read(BUFFER_SIZE)
            #while chunk:
               # conn.send(chunk)
                #chunk = file.read(BUFFER_SIZE)

#def viewserverfiles():
        # Get a list of available files on the server
    #filelist = ''
    #for file in os.listdir(os.getcwd()):
        #filelist += file + '\n'
       # conn.send(' '.join(filelist).encode())

#def viewlocalfiles():
   # file_list = ''
    #for file in os.listdir():
        #file_list += file + '\n'
        #conn.send(' '.join(file_list).encode())

def checkuserandpass(userandpass):
    userpasslist = userandpass.split('.!')
    userpassword = userpasslist[0]+userpasslist[1]
    code = userpasslist[2]
    username = userpasslist[0]
    if code == '0':
        with open('Credentials.txt', 'a') as f:
            f.write(userpassword + '\n')
            f.close()
            return 'account made', username

    else:
        with open('Credentials.txt', 'r') as f:
            for line in f:
                if userpassword in line:
                    f.close()
                    return 'successfully logged in', username
            f.close()
            return 'invalid credentials', username

def writetochatlog(user, message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    writetolog = f'{dt_string}: {user}: {message}'

    with open('chatlog.txt', 'a') as f:
        f.write(writetolog + '\n')
        f.close()
        return 'chat added'

def readchat():

    txt = Path('chatlog.txt').read_text()
    return txt

print('server starting')
start()