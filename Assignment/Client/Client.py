# Author information
# ...
#
#
#
import time
import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

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
        return f"{username} {password}.!{chosenoption}"




    elif chosenoption == str(1):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        return f"{username} {password}.!{chosenoption}"

    # Check if the entered username and password match any of the sets of credentials

while True:
    client = start()
    send('hello server I would like to make contact',client)
    chosenoption = input('')
    returnmsg = send(checkpassword(chosenoption), client)

    if returnmsg=='invalid credentials':
        continue








    # Ask the user to enter their username and password and give the possibility to create credentials




