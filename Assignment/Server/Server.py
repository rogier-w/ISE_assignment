# Author information
# ...
#
#
#

import socket

#Specification 1 Establish a connection to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the server's IP address and port number
server_host = "123.456.789.0" 
server_port = 1234  

s.bind((server_host, server_port))
s.listen()
connection, client_address = s.accept()
print(f"Connected by {client_adress}")
while True:
    data = connection.recv(1024)
    if data:
        print("Sending data to client")
        connection.sendall(data)
    if not data:
        print("No data from {client_adress}")
        break

connection.close
