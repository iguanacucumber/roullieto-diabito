import socket
from sys import argv
from time import sleep

from utils import args, clear


def send(msg):
    message = msg.strip().encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b" " * (1024 - len(send_length))
    client.send(send_length)
    client.send(message)
    received_message = client.recv(1024).decode("utf-8")
    print(received_message)
    return received_message


port, remote_ip = args(argv)

while True:
    clear()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 TCP
    client.connect((remote_ip, port))

    print((remote_ip, port))
    print("Login if user exists, automatically signs you up otherwise\n")
    res = send("[USERNAME]:" + input("Username: "))
    if res.startswith("[OK]"):
        print(send("[PASSWORD]:" + input("Password: ")))

    sleep(2)

    game = True
    while game == True:
        suj, content = handle_message(res)

        if suj == "[MAP]":
            base_map = strtolistoflists(content)
            print(base_map)
