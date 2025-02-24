import socket
from sys import argv

port = 8000
remote_ip = "127.0.0.1"

for i in range(len(argv)):
    if argv[i] == "-p" or argv[i] == "--port":
        port = argv[i + 1]
    elif argv[i] == "-i" or argv[i] == "--ip":
        remote_ip = argv[i + 1]
    elif argv[i] == "-h" or argv[i] == "--help":
        print("-i, --ip:   IP")
        print("-p, --port: PORT")
        exit()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Officially connecting to the server.
client.connect((remote_ip, port))


def send(msg):
    message = msg.encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b" " * (1024 - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(1024).decode("utf-8"))


while True:
    send(input("> "))
