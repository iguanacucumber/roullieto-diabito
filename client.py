import socket
from sys import argv

from utils import args

port, remote_ip = args(argv)


def send(msg):
    message = msg.encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b" " * (1024 - len(send_length))
    client.send(send_length)
    client.send(message)
    received_message = client.recv(1024).decode("utf-8")
    print(received_message)
    return received_message


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 TCP
client.connect((remote_ip, port))

logged_in = False

print("Login if user exists, automatically signs you up otherwise\n")
while True:
    res = send("[USERNAME]:" + input("Username: "))
    if res == "[OK]":
        res = send("[PASSWORD]:" + input("Password: "))
        if res == "[OK]":
            input("YES")
        else:
            input("FUCK")
