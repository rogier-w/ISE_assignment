# Author information
# ...
#
#
#

import socket
import time

#Specification 1 Establish a connection to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_host = "123.456.789.0" 
server_port = 1234  

s.connect((server_host, server_port))
message = "Hello"
print(f"Sending {message}")
s.sendall(message)
data = s.recv(1024)
print(f"Received {data}")

s.close()


#Specification 2 allow user to log in with credentials 
with open("Credentials.text", "r") as f:
    credentials = [line.strip().split(",") for line in f]

# Ask the user to enter their username and password and give the possibility to create credentials
checkforaccount = input("If you have not created an account yet please type 0, if you have an account please type 1.")

if checkforaccount == str(0):
    newusername = input("Enter your desired username here:")
    newpassword = input("Enter your desired password here:")

    with open("Credentials.text", "a") as appendnew:
        appendnew.write("\n")
        appendnew.append(str(newusername), str(newpassword))


if checkforaccount == str(1):
    username = input("Enter your username: ")
    password = input("Enter your password: ")

# Check if the entered username and password match any of the sets of credentials
for user, pwd in credentials:
    if username == user and password == pwd:
        print("Logged in!")
        break
else:
    print("Invalid credentials. Please try again.")
