"""
@author: Group 11 - Suus Plaum, Oscar Lodeizen, Julius Jorna, Milan Sonneveld, Rogier Wijnants
"""
import base64
import os
import time
import socket
from pathlib import Path
from struct import pack, unpack

import chardet

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

def sendfile(msg, client):

    client.sendall(msg)
    backmsg = (client.recv(2048).decode(FORMAT))


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
    with open(filename, 'rb') as f:

        txt = base64.b64encode(f.read())


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
                assert (len(filedata))
                length = pack('>Q', len(filedata))
                client.sendall(length)

                sendfile(filedata, client)
                print((client.recv(2048).decode(FORMAT)))


                send('test', client)
            elif l == '3':

                filename1 = input('')
                message = filename1.encode(FORMAT)

                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                client.send(send_length)
                client.send(message)
                bs = client.recv(8)
                (length,) = unpack('>Q', bs)
                length = int(length)

                numlist = [4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
                for x in numlist:

                    if length % x == 0:
                        num = x
                length = int(length / num)


                with open(filename1, 'wb') as file:
                    for x in range(length):
                        filedata = client.recv(num)

                        txt = base64.b64decode(filedata + b'==')

                        # Receive the file in chunks and write each chunk to the file
                        file.write(txt)
                msg='gelukt'
                message = msg.encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                client.send(send_length)
                client.send(message)
                client.recv(2048).decode(FORMAT)

                time.sleep(2)
                print(client.recv(2048).decode(FORMAT))


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
            elif l == '6':

                numfiles =t
                filelist=[]
                numfiles=int(numfiles)


                name = (client.recv(4096))

                name =name.decode(FORMAT)
                namelist = name.split()
                print(namelist)

                for y in namelist:

                    bs = client.recv(8)
                    print(bs)
                    (length,) = unpack('>Q', bs)
                    length = int(length)

                    numlist = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]
                    for z in numlist:

                        if length % z == 0:
                            num = z
                    length = int(length / num)

                    with open(y, 'wb') as file:

                        for x in range(length):
                            filedata = client.recv(num)

                            txt = base64.b64decode(filedata + b'==')

                            # Receive the file in chunks and write each chunk to the file
                            file.write(txt)
                print(filelist)
                print('downloading')

                print((client.recv(2048).decode(FORMAT)))






client.close()
