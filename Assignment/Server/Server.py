import socket
import threading
import hashlib
from datetime import datetime

HEADER = 64
PORT = 2088
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

        if msg_length:

            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")
            msgback = 'received message'
            if '.!' in msg:
                msgback, username = checkuserandpass(msg)
                conn.send(msgback.encode(FORMAT))
                if msgback == 'successfully logged in'or msgback == 'account made':
                    print('worked')
                else:
                    break

            elif msgback == DISCONNECT_MESSAGE:
                connected = False
                conn.close()

            conn.send('''You're succesfully logged in please select an option
                1 - chat
                2 - upload file
                3 - download files
                4 - view files'''.encode(FORMAT))
            msg_length = conn.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")


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
    username = userpasslist[1]
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
    chatlog = []
    with open('chatlog.txt', 'r') as f:
        for line in f:

            chatlog.append(line)
        f.close()
        return chatlog

print('server starting')
start()


