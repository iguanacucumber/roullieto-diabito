import csv
import os
import socket
import threading
from platform import system
from sys import argv
from time import sleep

from utils import args, clear, handle_message

# Crée la db selon l'OS
if system() == "Windows":
    base_folder = os.getenv("APPDATA")
else:  # Linux
    base_folder = os.path.expanduser("~/.local/share")

full_path = os.path.join(base_folder, "online-pacman")
os.makedirs(full_path, exist_ok=True)

db_path = os.path.join(full_path, "db.csv")

if not os.path.exists(db_path):  # Crée la db si elle n'existe pas
    with open(db_path, "w") as _:
        pass


locked_db = False  # Permet d'éviter que 2 utilisateurs écrivent dans la db en même temps


def db_writerow(end_row):
    global locked_db
    length = 0
    pos_user = -1
    db = []

    while locked_db:  # Permet d'éviter que 2 utilisateurs écrivent dans la db en même temps
        sleep(0.1)

    locked_db = True

    with open(db_path, mode="r") as file_read:
        for row in csv.reader(file_read):
            db.append(row)
            if row[0] == end_row[0]:
                pos_user = length
            length += 1

    with open(db_path, mode="w") as file_write:
        for row in db:
            if length == pos_user:
                csv.writer(file_write).writerow(end_row)
            else:
                csv.writer(file_write).writerow(row)

            length += 1
        if pos_user == -1:
            csv.writer(file_write).writerow(end_row)

    locked_db = False

    if pos_user == -1:
        return False  # user does not exist in db
    else:
        return True  # user exists


def handle_client(conn, addr):
    print(f"{addr[0]}:{addr[1]} connected.")  # IP:Port
    username = ""
    password = ""
    logged_in = False
    user_exists = False
    highscore = 0
    while True:
        msg_length = conn.recv(1024).decode("utf-8")
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode("utf-8")
            if msg == "[END]":
                break
                conn.send("[OK]".encode("utf-8"))
            elif msg.startswith("[USERNAME]:"):
                username = handle_message(msg)
                conn.send("[OK]".encode("utf-8"))
            elif msg.startswith("[PASSWORD]:"):
                password = handle_message(msg)
                with open(db_path, mode="r") as file:
                    for row in csv.reader(file):
                        if row[0] == username:
                            user_exists = True
                        if row[0] == username and row[1] == password:
                            logged_in = True
                            if row[3] == "True":
                                conn.send("[ERR]:Already logged in on another client".encode("utf-8"))
                                break

                            highscore = row[2]
                            db_writerow([username, password, highscore, "True"])  # logged_in = "True"

                            conn.send("[OK]:logged in".encode("utf-8"))
                            break
                    if not logged_in and not user_exists:
                        db_writerow([username, password, highscore, "True"])
                        conn.send("[OK]".encode("utf-8"))
                    elif logged_in:
                        break
                    else:
                        conn.send("[ERR]: wrong password".encode("utf-8"))

            elif msg.startswith("[OTHER]:"):
                conn.send("[OK]".encode("utf-8"))
            else:
                conn.send("[ERR]".encode("utf-8"))

            print(f"{addr[0]}:{addr[1]}> {msg}")

    conn.close()


port, host = args(argv)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 TCP
server.bind((host, port))

server.listen()
clear()
print(f"Server is listening on {host}")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
