import csv
import socket
import threading
from sys import argv

from utils import args

port, host = args(argv)


def db_writerow(end_row):
    length = 0
    pos_user = -1
    with open("db.csv", mode="r") as file_read:
        for row in csv.reader(file_read):
            length += 1
            if row[0] == end_row[0]:
                pos_user = length

    with open("db.csv", mode="w") as file_write:
        with open("db.csv", mode="r") as file_read:
            csv.writer(file_write).writerow(
                ["username", "password", "highscore", "is-logged-in"]
            )
            for row in csv.reader(file_read):
                length += 1
                if length == pos_user:
                    csv.writer(file_write).writerow(end_row)
                else:
                    csv.writer(file_write).writerow(row)
            if pos_user == -1:
                csv.writer(file_write).writerow(end_row)

    if pos_user == -1:
        return False  # Doesn't exist in db
    else:
        return True  # Exists


def handle_message(msg):
    past_header = False
    message = ""
    for character in msg:
        if past_header:
            message += character

        if character == ":":
            past_header = True

    return message


def handle_client(conn, addr):
    print(f"{addr[0]}:{addr[1]} connected.")  # IP:Port
    username = ""
    password = ""
    logged_in = False
    user_exists = False
    highscore = 0
    connected = True
    while connected:
        msg_length = conn.recv(1024).decode("utf-8")
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode("utf-8")
            if msg == "[END]":
                connected = False
                conn.send("[OK]".encode("utf-8"))
            elif msg.startswith("[USERNAME]:"):
                username = handle_message(msg)
                conn.send("[OK]".encode("utf-8"))
            elif msg.startswith("[PASSWORD]:"):
                password = handle_message(msg)
                with open("db.csv", mode="r") as file:
                    for row in csv.reader(file):
                        if row[0] == username:
                            user_exists = True
                        if row[0] == username and row[1] == password:
                            logged_in = True
                            highscore = row[3]
                            db_writerow([username, password, highscore, logged_in])

                            conn.send("[OK]".encode("utf-8"))
                            break
                    if not logged_in and not user_exists:
                        db_writerow([username, password, highscore, logged_in])
                        conn.send("[OK]".encode("utf-8"))
                    else:
                        conn.send("[ERR]".encode("utf-8"))

            elif msg == "[OTHER]:":
                conn.send("[OK]".encode("utf-8"))

            print(f"{addr[0]}:{addr[1]}> {msg}")

    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 TCP
server.bind((host, port))

server.listen()
print(f"Server is listening on {host}")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
