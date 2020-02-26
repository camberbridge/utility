from socket import socket, AF_INET, SOCK_DGRAM

HOST = ''
PORT = 20000
#ADDRESS = "192.168.64.1"
ADDRESS = "127.0.0.1"

s = socket(AF_INET, SOCK_DGRAM)

while True:
    msg = input("> ")
    s.sendto(msg.encode(), (ADDRESS, PORT))

s.close()
