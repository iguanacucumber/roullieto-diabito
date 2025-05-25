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
lobby_lock = threading.Lock()


def send(message, conn):
    conn.send(message.encode("utf-8"))


def get_lobbies():
    with lobby_lock:
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


def get_lobby_info(lobby_id):
    with lobby_lock:
        if lobby_id in lobbies:
            return lobbies[lobby_id].copy()
        return None


def create_lobby(name, max_players, creator):
    global lobby_counter
    with lobby_lock:
        lobby_id = lobby_counter
        lobby_counter += 1

        lobbies[lobby_id] = {"name": name, "max_players": max_players, "players": [creator], "status": "waiting", "created_at": time.time(), "host": creator}

    with open(lobbies_db_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([lobby_id, name, max_players, creator, "waiting", time.time()])

    return lobby_id


def remove_user_from_all_lobbies(username):
    with lobby_lock:
        lobbies_to_remove = []
        for lobby_id, lobby in lobbies.items():
            if username in lobby["players"]:
                lobby["players"].remove(username)

                if lobby.get("host") == username and lobby["players"]:
                    lobby["host"] = lobby["players"][0]

                if not lobby["players"]:
                    lobbies_to_remove.append(lobby_id)

        for lobby_id in lobbies_to_remove:
            if lobby_id in lobbies:
                del lobbies[lobby_id]


def join_lobby(lobby_id, username):
    with lobby_lock:
        if lobby_id not in lobbies:
            return False

        lobby = lobbies[lobby_id]

        if len(lobby["players"]) >= lobby["max_players"]:
            return False

        if lobby["status"] != "waiting":
            return False

        if username in lobby["players"]:
            return True

        remove_user_from_all_lobbies_unlocked(username)
        lobby["players"].append(username)
        return True


def remove_user_from_all_lobbies_unlocked(username):
    lobbies_to_remove = []
    for lobby_id, lobby in lobbies.items():
        if username in lobby["players"]:
            lobby["players"].remove(username)

            if lobby.get("host") == username and lobby["players"]:
                lobby["host"] = lobby["players"][0]

            if not lobby["players"]:
                lobbies_to_remove.append(lobby_id)

    for lobby_id in lobbies_to_remove:
        if lobby_id in lobbies:
            del lobbies[lobby_id]


def leave_lobby(lobby_id, username):
    with lobby_lock:
        if lobby_id not in lobbies:
            return False

        lobby = lobbies[lobby_id]
        if username not in lobby["players"]:
            return False

        lobby["players"].remove(username)

        if lobby.get("host") == username and lobby["players"]:
            lobby["host"] = lobby["players"][0]

        if not lobby["players"]:
            del lobbies[lobby_id]

        return True


def start_game(lobby_id, username):
    with lobby_lock:
        if lobby_id not in lobbies:
            return False

        lobby = lobbies[lobby_id]
        if lobby.get("host") != username:
            return False

        if len(lobby["players"]) < 2:
            return False

        lobby["status"] = "playing"
        return True


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
            elif header == "GET_LOBBY_INFO":
                if logged_in:
                    try:
                        lobby_id = int(message)
                        lobby_info = get_lobby_info(lobby_id)
                        if lobby_info:
                            send(f"[LOBBY_INFO]:{json.dumps(lobby_info)}", conn)
                        else:
                            send("[ERR]:lobby not found", conn)
                    except:
                        send("[ERR]:invalid lobby id", conn)
                else:
                    send("[ERR]:not logged in", conn)
            elif header == "CREATE_LOBBY":
                if logged_in:
                    try:
                        parts = message.split(":")
                        lobby_name = parts[0]
                        max_players = int(parts[1])
                        lobby_id = create_lobby(lobby_name, max_players, username)
                        current_lobby = lobby_id
                        send(f"[LOBBY_CREATED]:{lobby_id}", conn)
                    except:
                        send("[ERR]:invalid lobby data", conn)
                else:
                    send("[ERR]:not logged in", conn)
            elif header == "JOIN_LOBBY":
                if logged_in:
                    try:
                        lobby_id = int(message)
                        if join_lobby(lobby_id, username):
                            current_lobby = lobby_id
                            send(f"[LOBBY_JOINED]:{lobby_id}", conn)
                        else:
                            lobby_info = get_lobby_info(lobby_id)
                            if not lobby_info:
                                send("[ERR]:lobby not found", conn)
                            elif len(lobby_info["players"]) >= lobby_info["max_players"]:
                                send("[ERR]:lobby is full", conn)
                            elif lobby_info["status"] != "waiting":
                                send("[ERR]:game already started", conn)
                            else:
                                send("[ERR]:could not join lobby", conn)
                    except:
                        send("[ERR]:invalid lobby id", conn)
                else:
                    send("[ERR]:not logged in", conn)
            elif header == "LEAVE_LOBBY":
                if logged_in and current_lobby:
                    try:
                        lobby_id = int(message) if message.strip() else current_lobby
                        if leave_lobby(lobby_id, username):
                            current_lobby = None
                            send("[OK]:left lobby", conn)
                        else:
                            send("[ERR]:could not leave lobby", conn)
                    except:
                        if leave_lobby(current_lobby, username):
                            current_lobby = None
                            send("[OK]:left lobby", conn)
                        else:
                            send("[ERR]:could not leave lobby", conn)
                else:
                    send("[ERR]:not in lobby", conn)
            elif header == "START_GAME":
                if logged_in and current_lobby:
                    try:
                        lobby_id = int(message) if message.strip() else current_lobby
                        if start_game(lobby_id, username):
                            send("[GAME_STARTED]:game started", conn)
                        else:
                            lobby_info = get_lobby_info(lobby_id)
                            if not lobby_info:
                                send("[ERR]:lobby not found", conn)
                            elif lobby_info.get("host") != username:
                                send("[ERR]:only host can start game", conn)
                            elif len(lobby_info["players"]) < 2:
                                send("[ERR]:need at least 2 players", conn)
                            else:
                                send("[ERR]:cannot start game", conn)
                    except:
                        send("[ERR]:invalid lobby id", conn)
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
