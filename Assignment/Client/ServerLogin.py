"""
@author: Group 11 - Suus Plaum, Oscar Lodeizen, Julius Jorna, Milan Sonneveld, Rogier Wijnants
"""
import base64
import os
import socket
import threading
import time
import hashlib
from datetime import datetime
from pathlib import Path

import chardet

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
                    conn.close()

            while True:
                conn.send('''Please select an option:
    1 - chat
    2 - upload file
    3 - download files
    4 - view files
    5 - disconnect
Please enter a number: '''.encode(FORMAT))
                msg_length1 = conn.recv(HEADER).decode(FORMAT)
                if msg_length1:

                    msg_length1 = int(msg_length1)
                    msg1 = conn.recv(msg_length1).decode(FORMAT)
                    print(f"[{addr}] {msg1}")

                    if '1' == msg1:
                        chat = readchat()

                        conn.send(chat.encode(FORMAT))
                        msg_length2 = conn.recv(HEADER).decode(FORMAT)
                        msg_length2 = int(msg_length2)
                        msg = conn.recv(msg_length2).decode(FORMAT)
                        print(f"[{addr}] {msg}")
                        writetochatlog(username, msg)
                    elif '2' == msg1:
                        conn.send('Please enter a filename: '.encode(FORMAT))
                        msg_length1 = conn.recv(HEADER).decode(FORMAT)
                        msg_length1 = int(msg_length1)
                        filename = conn.recv(msg_length1).decode(FORMAT)
                        print(filename)
                        conn.send('uploading file'.encode(FORMAT))


                        filedata = conn.recv(4096*4096*32)


                        with open(filename, 'wb') as file:
                            txt = base64.b64decode(filedata+b'==')

                            # Receive the file in chunks and write each chunk to the file
                            file.write(txt)

                    elif '3' == msg1:

                        conn.send('Please enter a filename: '.encode(FORMAT))
                        msg_length1 = conn.recv(HEADER).decode(FORMAT)
                        msg_length1 = int(msg_length1)

                        filename1 = conn.recv(msg_length1).decode(FORMAT)
                        print(filename1)
                        if not os.path.exists(filename1):
                            # Send an error message to the client
                            conn.send('Error: File does not exist'.encode())
                        else:
                            # Open the file for reading
                            data = readfile(filename1)
                            conn.send(data)

                    elif '4' == msg1:
                        conn.send('Do you want to view server files or local files?\n1 - Server\n2 - Local'.encode(FORMAT))
                        msg_length3 = conn.recv(HEADER).decode(FORMAT)


                        msg_length3 = int(msg_length3)
                        msg = conn.recv(msg_length3).decode(FORMAT)
                        print(msg)
                        if msg == '1':
                            filelist = ''
                            for file in os.listdir(os.getcwd()):

                                filelist += file + '\n'
                            conn.send(('Files: \n' +filelist).encode(FORMAT))

                    elif msg1 == '5':

                        conn.close()




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

    txt = Path('chatlog.txt').read_text() +'\n please enter a message '
    return txt
def readfile(filename):
    with open(filename, 'rb') as f:

        txt = base64.b64encode(f.read())


    return txt

print('server starting')
start()
