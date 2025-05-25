import csv
import json
import socket
import threading
import time
from sys import argv

from map import map
from utils import args, clear, create_db, db_writerow, handle_message

map_json = json.dumps(map)

users_db_path = create_db("users.csv")
lobbies_db_path = create_db("lobbies.csv")

lobbies = {}
lobby_counter = 1
connected_users = {}


def send(message, conn):
    conn.send(message.encode("utf-8"))


def get_lobbies():
    lobby_list = []
    for lobby_id, lobby_data in lobbies.items():
        lobby_list.append(
            {
                "id": lobby_id,
                "name": lobby_data["name"],
                "players": len(lobby_data["players"]),
                "max_players": lobby_data["max_players"],
                "status": lobby_data["status"],
            }
        )
    return lobby_list


def create_lobby(name, max_players, creator):
    global lobby_counter
    lobby_id = lobby_counter
    lobby_counter += 1

    lobbies[lobby_id] = {"name": name, "max_players": max_players, "players": [creator], "status": "waiting", "created_at": time.time()}

    with open(lobbies_db_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([lobby_id, name, max_players, creator, "waiting", time.time()])

    return lobby_id


def remove_user_from_all_lobbies(username):
    lobbies_to_remove = []
    for lobby_id, lobby in lobbies.items():
        if username in lobby["players"]:
            lobby["players"].remove(username)
            if not lobby["players"]:
                lobbies_to_remove.append(lobby_id)

    for lobby_id in lobbies_to_remove:
        del lobbies[lobby_id]


def join_lobby(lobby_id, username):
    if lobby_id in lobbies:
        lobby = lobbies[lobby_id]

        remove_user_from_all_lobbies(username)

        if len(lobby["players"]) < lobby["max_players"]:
            lobby["players"].append(username)
            return True
    return False


def leave_lobby(lobby_id, username):
    if lobby_id in lobbies:
        lobby = lobbies[lobby_id]
        if username in lobby["players"]:
            lobby["players"].remove(username)
            if not lobby["players"]:
                del lobbies[lobby_id]
            return True
    return False


def cleanup_user(username):
    remove_user_from_all_lobbies(username)
    if username in connected_users:
        del connected_users[username]

    with open(users_db_path, mode="r") as file:
        rows = list(csv.reader(file))

    with open(users_db_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        for row in rows:
            if row and len(row) >= 4:
                if row[0] == username:
                    row[3] = "False"
                writer.writerow(row)


def handle_client(conn, addr):
    print(f"{addr[0]}:{addr[1]} connected.")
    username = ""
    password = ""
    logged_in = False
    user_exists = False
    highscore = 0
    current_lobby = None

    try:
        while True:
            try:
                msg_length = conn.recv(1024).decode("utf-8")
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                break

            if not msg_length:
                continue

            try:
                msg_length = int(msg_length.strip())
                response = conn.recv(msg_length).decode("utf-8")
            except (ValueError, ConnectionResetError, ConnectionAbortedError, OSError):
                break

            message, header = handle_message(response)

            if header == "END":
                if current_lobby:
                    leave_lobby(current_lobby, username)
                send("[OK]", conn)
                break
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
                            if len(row) > 3 and row[3] == "True":
                                send("[ERR]:Already logged in on another client", conn)
                                break

                            highscore = row[2] if len(row) > 2 else "0"
                            db_writerow([username, password, highscore, "True"], users_db_path)
                            connected_users[username] = conn

                            send("[OK]:logged in", conn)
                            break

                if not logged_in and not user_exists:
                    db_writerow([username, password, str(highscore), "True"], users_db_path)
                    connected_users[username] = conn
                    logged_in = True
                    send("[OK]:signed up", conn)
                elif not logged_in:
                    send("[ERR]:wrong password", conn)
            elif header == "GET_LOBBIES":
                if logged_in:
                    lobby_list = get_lobbies()
                    send(f"[LOBBIES]:{json.dumps(lobby_list)}", conn)
                else:
                    send("[ERR]:not logged in", conn)
            elif header == "CREATE_LOBBY":
                try:
                    parts = message.split(":")
                    lobby_name = parts[0]
                    max_players = int(parts[1])
                    lobby_id = create_lobby(lobby_name, max_players, username)
                    current_lobby = lobby_id
                    send(f"[LOBBY_CREATED]:{lobby_id}", conn)
                except:
                    send("[ERR]:invalid lobby data", conn)
            elif header == "JOIN_LOBBY":
                if logged_in:
                    try:
                        lobby_id = int(message)
                        if join_lobby(lobby_id, username):
                            current_lobby = lobby_id
                            send(f"[LOBBY_JOINED]:{lobby_id}", conn)
                        else:
                            send("[ERR]:could not join lobby", conn)
                    except:
                        send("[ERR]:invalid lobby id", conn)
                else:
                    send("[ERR]:not logged in", conn)
            elif header == "LEAVE_LOBBY":
                if logged_in and current_lobby:
                    if leave_lobby(current_lobby, username):
                        current_lobby = None
                        send("[OK]:left lobby", conn)
                    else:
                        send("[ERR]:could not leave lobby", conn)
                else:
                    send("[ERR]:not in lobby", conn)
            else:
                send("[ERR]:unknown command", conn)

            print(f"{addr[0]}:{addr[1]}> {response}")

    except Exception as e:
        print(f"Error handling client {addr[0]}:{addr[1]}: {e}")
    finally:
        print(f"{addr[0]}:{addr[1]} disconnected.")
        if username:
            cleanup_user(username)
        try:
            conn.close()
        except:
            pass


port, host = args(argv)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))

server.listen()
clear()
print(f"Server is listening on {host}:{port}")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
