import csv
import json
import socket
import threading
from sys import argv

from map import map
from utils import args, clear, create_db, db_writerow, handle_message

map_json = json.dumps(map)

users_db_path = create_db("users.csv")
create_db("lobbies.csv")


def send(message, conn):
    conn.send(message.encode("utf-8"))


def handle_client(conn, addr):
    print(f"{addr[0]}:{addr[1]} connected.")  # IP:Port
    username = ""
    password = ""
    logged_in = False
    user_exists = False
    highscore = 0
    while True:
        msg_length = conn.recv(1024).decode("utf-8")
        if not msg_length:
            continue

        msg_length = int(msg_length)
        response = conn.recv(msg_length).decode("utf-8")
        message, header = handle_message(response)
        if header == "END":
            break
            send("[OK]", conn)
        elif header == "USERNAME":
            username = message
            send("[OK]", conn)
        elif header == "PASSWORD":
            password = message
            with open(users_db_path, mode="r") as file:
                for row in csv.reader(file):
                    if row[0] == username:
                        user_exists = True
                    if row[0] == username and row[1] == password:
                        logged_in = True
                        if row[3] == "True":
                            send("[ERR]:Already logged in on another client", conn)
                            break

                        highscore = row[2]
                        db_writerow([username, password, highscore, "True"], users_db_path)  # logged_in = "True"

                        send("[OK]:logged in", conn)
                        send("[MAP]:" + map_json, conn)
                        break
                if not logged_in and not user_exists:
                    db_writerow([username, password, highscore, "True"], users_db_path)
                    logged_in = True
                    send("[OK]:signed up", conn)
                    send("[MAP]:" + map_json, conn)
                else:
                    send("[ERR]:wrong password", conn)
        elif header == "DISCONNECT":
            db_writerow([username, password, highscore, "False"])
            return
        else:
            send("[ERR]", conn)

        print(f"{addr[0]}:{addr[1]}> {response}")

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
