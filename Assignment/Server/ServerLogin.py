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
from struct import unpack, pack

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
    6 - batch
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
                        msg_length5 = conn.recv(HEADER).decode(FORMAT)
                        msg_length5 = int(msg_length5)
                        filename = conn.recv(msg_length5).decode(FORMAT)
                        print(filename)
                        t0 = time.time()
                        conn.send('uploading file'.encode(FORMAT))
                        bs = conn.recv(8)
                        (length,) = unpack('>Q', bs)
                        length = int(length)

                        numlist = [4,8,16,32,64,128,256,512,1024,2048,4096,8192]
                        for x in numlist:

                            if length % x == 0:


                                num = x
                        length = int(length / num)


                        with open(filename, 'wb') as file:
                            for x in range(length):
                                filedata = conn.recv(num)

                                txt = base64.b64decode(filedata+b'==')

                                # Receive the file in chunks and write each chunk to the file
                                file.write(txt)
                        t1 = time.time()
                        total = t1 - t0
                        conn.send(total.encode(FORMAT))




                    elif '3' == msg1:

                        conn.send('Please enter a filename: '.encode(FORMAT))
                        msg_length4 = conn.recv(HEADER).decode(FORMAT)
                        msg_length4 = int(msg_length4)

                        filename1 = conn.recv(msg_length4).decode(FORMAT)
                        print(filename1)
                        if not os.path.exists(filename1):
                            # Send an error message to the client
                            conn.send('Error: File does not exist'.encode())
                        else:
                            # Open the file for reading
                            data = readfile(filename1)
                            length = pack('>Q', len(data))
                            conn.sendall(length)
                            conn.sendall(data)

                    elif '4' == msg1:
                        conn.send(
                            'Do you want to view server files or local files?\n1 - Server\n2 - Local'.encode(FORMAT))
                        msg_length3 = conn.recv(HEADER).decode(FORMAT)

                        msg_length3 = int(msg_length3)
                        msg = conn.recv(msg_length3).decode(FORMAT)
                        print(msg)
                        if msg == '1':
                            filelist = ''
                            for file in os.listdir(os.getcwd()):
                                filelist += file + '\n'
                            conn.send(('Files: \n' + filelist).encode(FORMAT))

                    elif msg1 == '5':

                        conn.close()
                    elif '6' == msg1:
                        t0 = time.time()
                        a=0
                        filelist=[]
                        for x in os.listdir(os.getcwd()):
                            a+=1
                            filelist.append(x)
                        print(a)

                        conn.send(str(a).encode(FORMAT))
                        print(filelist)

                        filelist1 =' '.join(filelist)
                        print(filelist1)
                        conn.send(filelist1.encode(FORMAT))
                        for x in filelist:

                            data = readfile(x)

                            length = pack('>Q', len(data))

                            conn.sendall(length)
                            conn.sendall(data)


                        t1 = time.time()

                        total = t1 - t0
                        conn.send(str(total).encode(FORMAT))



def login(conn):
    conn.send(
        """please login to continue, if you already have an account press 1 if you want to make a new account press 0 """
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
    userpassword = userpasslist[0] + userpasslist[1]
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
    txt = Path('chatlog.txt').read_text() + '\n please enter a message '
    return txt


def readfile(filename):
    with open(filename, 'rb') as f:
        txt = base64.b64encode(f.read())

    return txt


print('server starting')
start()
