import csv
import json
import socket
import threading
import time
from datetime import datetime
from sys import argv

from map import map
from utils import args, clear, colors, create_db, db_writerow, handle_message

map_json = json.dumps(map)

users_db_path = create_db("users.csv")
lobbies_db_path = create_db("lobbies.csv")

lobbies = {}
lobby_counter = 1
connected_users = {}
lobby_lock = threading.Lock()


def log_with_timestamp(message, color="RESET"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{colors['GREY']}[{timestamp}]{colors['RESET']} {colors[color]}{message}{colors['RESET']}")


def log_user_action(username, action, details=""):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if details:
        print(
            f"{colors['GREY']}[{timestamp}]{colors['RESET']} {colors['BLUE']}[USER]{colors['RESET']} {colors['BOLD']}{username}{colors['RESET']}: {action} - {details}"
        )
    else:
        print(f"{colors['GREY']}[{timestamp}]{colors['RESET']} {colors['BLUE']}[USER]{colors['RESET']} {colors['BOLD']}{username}{colors['RESET']}: {action}")


def log_lobby_action(lobby_id, action, details=""):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if details:
        print(f"{colors['GREY']}[{timestamp}]{colors['RESET']} {colors['PURPLE']}[LOBBY {lobby_id}]{colors['RESET']} {action} - {details}")
    else:
        print(f"{colors['GREY']}[{timestamp}]{colors['RESET']} {colors['PURPLE']}[LOBBY {lobby_id}]{colors['RESET']} {action}")


def log_connection(addr, action, color="GREEN"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{colors['GREY']}[{timestamp}]{colors['RESET']} {colors[color]}[CONN]{colors['RESET']} {addr[0]}:{addr[1]} {action}")


def print_server_stats():
    with lobby_lock:
        active_lobbies = len(lobbies)
        total_players = sum(len(lobby["players"]) for lobby in lobbies.values())
        active_connections = len(connected_users)

    print(f"\n{colors['YELLOW']}{'=' * 50}{colors['RESET']}")
    print(f"{colors['YELLOW']}SERVER STATUS{colors['RESET']}")
    print(f"{colors['YELLOW']}{'=' * 50}{colors['RESET']}")
    print(f"{colors['GREEN']}Active Connections: {colors['BOLD']}{active_connections}{colors['RESET']}")
    print(f"{colors['PURPLE']}Active Lobbies: {colors['BOLD']}{active_lobbies}{colors['RESET']}")
    print(f"{colors['BLUE']}Players in Lobbies: {colors['BOLD']}{total_players}{colors['RESET']}")

    if lobbies:
        print(f"\n{colors['YELLOW']}LOBBY DETAILS:{colors['RESET']}")
        for lobby_id, lobby_data in lobbies.items():
            status_color = "GREEN" if lobby_data["status"] == "waiting" else "RED"
            print(
                f"  {colors['PURPLE']}#{lobby_id}{colors['RESET']} {lobby_data['name']} "
                f"({colors['BOLD']}{len(lobby_data['players'])}/{lobby_data['max_players']}{colors['RESET']}) "
                f"[{colors[status_color]}{lobby_data['status'].upper()}{colors['RESET']}] "
                f"Host: {colors['BOLD']}{lobby_data['host']}{colors['RESET']}"
            )

    if connected_users:
        print(f"\n{colors['YELLOW']}CONNECTED USERS:{colors['RESET']}")
        for username in connected_users.keys():
            user_lobby = None
            for lobby_id, lobby_data in lobbies.items():
                if username in lobby_data["players"]:
                    user_lobby = lobby_id
                    break

            if user_lobby:
                print(f"  {colors['BOLD']}{username}{colors['RESET']} - In lobby #{user_lobby}")
            else:
                print(f"  {colors['BOLD']}{username}{colors['RESET']} - In menu")

    print(f"{colors['YELLOW']}{'=' * 50}{colors['RESET']}\n")


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

    log_lobby_action(lobby_id, "CREATED", f"'{name}' by {creator} (max: {max_players})")
    return lobby_id


def remove_user_from_all_lobbies(username):
    with lobby_lock:
        lobbies_to_remove = []
        for lobby_id, lobby in lobbies.items():
            if username in lobby["players"]:
                lobby["players"].remove(username)
                log_lobby_action(lobby_id, "PLAYER LEFT", f"{username} removed from lobby")

                if lobby.get("host") == username and lobby["players"]:
                    new_host = lobby["players"][0]
                    lobby["host"] = new_host
                    log_lobby_action(lobby_id, "HOST CHANGED", f"New host: {new_host}")

                if not lobby["players"]:
                    lobbies_to_remove.append(lobby_id)

        for lobby_id in lobbies_to_remove:
            if lobby_id in lobbies:
                log_lobby_action(lobby_id, "DESTROYED", "No players remaining")
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
        log_lobby_action(lobby_id, "PLAYER JOINED", f"{username} joined ({len(lobby['players'])}/{lobby['max_players']})")
        return True


def remove_user_from_all_lobbies_unlocked(username):
    lobbies_to_remove = []
    for lobby_id, lobby in lobbies.items():
        if username in lobby["players"]:
            lobby["players"].remove(username)
            log_lobby_action(lobby_id, "PLAYER LEFT", f"{username} removed from lobby")

            if lobby.get("host") == username and lobby["players"]:
                new_host = lobby["players"][0]
                lobby["host"] = new_host
                log_lobby_action(lobby_id, "HOST CHANGED", f"New host: {new_host}")

            if not lobby["players"]:
                lobbies_to_remove.append(lobby_id)

    for lobby_id in lobbies_to_remove:
        if lobby_id in lobbies:
            log_lobby_action(lobby_id, "DESTROYED", "No players remaining")
            del lobbies[lobby_id]


def leave_lobby(lobby_id, username):
    with lobby_lock:
        if lobby_id not in lobbies:
            return False

        lobby = lobbies[lobby_id]
        if username not in lobby["players"]:
            return False

        lobby["players"].remove(username)
        log_lobby_action(lobby_id, "PLAYER LEFT", f"{username} left ({len(lobby['players'])}/{lobby['max_players']})")

        if lobby.get("host") == username and lobby["players"]:
            new_host = lobby["players"][0]
            lobby["host"] = new_host
            log_lobby_action(lobby_id, "HOST CHANGED", f"New host: {new_host}")

        if not lobby["players"]:
            log_lobby_action(lobby_id, "DESTROYED", "No players remaining")
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
        log_lobby_action(lobby_id, "GAME STARTED", f"Started by {username} with {len(lobby['players'])} players")
        return True


def cleanup_user(username):
    if username:
        log_user_action(username, "CLEANUP", "Removing from all lobbies and disconnecting")

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
    log_connection(addr, "CONNECTED")
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
            except (ConnectionResetError, ConnectionAbortedError, OSError) as e:
                log_with_timestamp(f"Connection error from {addr[0]}:{addr[1]}: {e}", "RED")
                break

            if not msg_length:
                continue

            try:
                msg_length = int(msg_length.strip())
                response = conn.recv(msg_length).decode("utf-8")
            except (ValueError, ConnectionResetError, ConnectionAbortedError, OSError) as e:
                log_with_timestamp(f"Message error from {addr[0]}:{addr[1]}: {e}", "RED")
                break

            message, header = handle_message(response)

            if header == "END":
                if current_lobby:
                    leave_lobby(current_lobby, username)
                send("[OK]", conn)
                log_user_action(username if username else f"{addr[0]}:{addr[1]}", "DISCONNECTED", "Clean disconnect")
                break
            elif header == "USERNAME":
                username = message
                send("[OK]", conn)
                log_user_action(username, "USERNAME SET")
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
                                log_user_action(username, "LOGIN FAILED", "Already logged in elsewhere")
                                break

                            highscore = row[2] if len(row) > 2 else "0"
                            db_writerow([username, password, highscore, "True"], users_db_path)
                            connected_users[username] = conn

                            send("[OK]:logged in", conn)
                            log_user_action(username, "LOGGED IN", f"Highscore: {highscore}")
                            print_server_stats()
                            break

                if not logged_in and not user_exists:
                    db_writerow([username, password, str(highscore), "True"], users_db_path)
                    connected_users[username] = conn
                    logged_in = True
                    send("[OK]:signed up", conn)
                    log_user_action(username, "SIGNED UP", "New user registered")
                    print_server_stats()
                elif not logged_in:
                    send("[ERR]:wrong password", conn)
                    log_user_action(username, "LOGIN FAILED", "Wrong password")
            elif header == "GET_LOBBIES":
                if logged_in:
                    lobby_list = get_lobbies()
                    send(f"[LOBBIES]:{json.dumps(lobby_list)}", conn)
                    log_user_action(username, "REQUESTED LOBBIES", f"Sent {len(lobby_list)} lobbies")
                else:
                    send("[ERR]:not logged in", conn)
            elif header == "GET_LOBBY_INFO":
                if logged_in:
                    try:
                        lobby_id = int(message)
                        lobby_info = get_lobby_info(lobby_id)
                        if lobby_info:
                            send(f"[LOBBY_INFO]:{json.dumps(lobby_info)}", conn)
                            log_user_action(username, "REQUESTED LOBBY INFO", f"Lobby #{lobby_id}")
                        else:
                            send("[ERR]:lobby not found", conn)
                            log_user_action(username, "LOBBY INFO FAILED", f"Lobby #{lobby_id} not found")
                    except:
                        send("[ERR]:invalid lobby id", conn)
                        log_user_action(username, "LOBBY INFO FAILED", "Invalid lobby ID")
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
                        log_user_action(username, "CREATED LOBBY", f"#{lobby_id} '{lobby_name}' (max: {max_players})")
                        print_server_stats()
                    except:
                        send("[ERR]:invalid lobby data", conn)
                        log_user_action(username, "LOBBY CREATION FAILED", "Invalid data")
                else:
                    send("[ERR]:not logged in", conn)
            elif header == "JOIN_LOBBY":
                if logged_in:
                    try:
                        lobby_id = int(message)
                        if join_lobby(lobby_id, username):
                            current_lobby = lobby_id
                            send(f"[LOBBY_JOINED]:{lobby_id}", conn)
                            log_user_action(username, "JOINED LOBBY", f"#{lobby_id}")
                            print_server_stats()
                        else:
                            lobby_info = get_lobby_info(lobby_id)
                            if not lobby_info:
                                send("[ERR]:lobby not found", conn)
                                log_user_action(username, "JOIN FAILED", f"Lobby #{lobby_id} not found")
                            elif len(lobby_info["players"]) >= lobby_info["max_players"]:
                                send("[ERR]:lobby is full", conn)
                                log_user_action(username, "JOIN FAILED", f"Lobby #{lobby_id} is full")
                            elif lobby_info["status"] != "waiting":
                                send("[ERR]:game already started", conn)
                                log_user_action(username, "JOIN FAILED", f"Lobby #{lobby_id} game in progress")
                            else:
                                send("[ERR]:could not join lobby", conn)
                                log_user_action(username, "JOIN FAILED", f"Lobby #{lobby_id} unknown error")
                    except:
                        send("[ERR]:invalid lobby id", conn)
                        log_user_action(username, "JOIN FAILED", "Invalid lobby ID")
                else:
                    send("[ERR]:not logged in", conn)
            elif header == "LEAVE_LOBBY":
                if logged_in and current_lobby:
                    try:
                        lobby_id = int(message) if message.strip() else current_lobby
                        if leave_lobby(lobby_id, username):
                            current_lobby = None
                            send("[OK]:left lobby", conn)
                            log_user_action(username, "LEFT LOBBY", f"#{lobby_id}")
                            print_server_stats()
                        else:
                            send("[ERR]:could not leave lobby", conn)
                            log_user_action(username, "LEAVE FAILED", f"Lobby #{lobby_id}")
                    except:
                        if leave_lobby(current_lobby, username):
                            current_lobby = None
                            send("[OK]:left lobby", conn)
                            log_user_action(username, "LEFT LOBBY", f"#{current_lobby}")
                            print_server_stats()
                        else:
                            send("[ERR]:could not leave lobby", conn)
                            log_user_action(username, "LEAVE FAILED", "Current lobby")
                else:
                    send("[ERR]:not in lobby", conn)
            elif header == "START_GAME":
                if logged_in and current_lobby:
                    try:
                        lobby_id = int(message) if message.strip() else current_lobby
                        if start_game(lobby_id, username):
                            send("[GAME_STARTED]:game started", conn)
                            log_user_action(username, "STARTED GAME", f"Lobby #{lobby_id}")
                            print_server_stats()
                        else:
                            lobby_info = get_lobby_info(lobby_id)
                            if not lobby_info:
                                send("[ERR]:lobby not found", conn)
                                log_user_action(username, "START FAILED", f"Lobby #{lobby_id} not found")
                            elif lobby_info.get("host") != username:
                                send("[ERR]:only host can start game", conn)
                                log_user_action(username, "START FAILED", f"Not host of lobby #{lobby_id}")
                            elif len(lobby_info["players"]) < 2:
                                send("[ERR]:need at least 2 players", conn)
                                log_user_action(username, "START FAILED", f"Not enough players in lobby #{lobby_id}")
                            else:
                                send("[ERR]:cannot start game", conn)
                                log_user_action(username, "START FAILED", f"Unknown error for lobby #{lobby_id}")
                    except:
                        send("[ERR]:invalid lobby id", conn)
                        log_user_action(username, "START FAILED", "Invalid lobby ID")
                else:
                    send("[ERR]:not in lobby", conn)
            elif header == "DISCONNECT":
                cleanup_user(username)
                username = ""
                password = ""
                conn.close()
            else:
                send("[ERR]:unknown command", conn)
                log_user_action(username if username else f"{addr[0]}:{addr[1]}", "UNKNOWN COMMAND", header)

            log_with_timestamp(f"{addr[0]}:{addr[1]} [{username if username else 'ANON'}]> {response}", "GREY")

    except Exception as e:
        log_with_timestamp(f"Error handling client {addr[0]}:{addr[1]}: {e}", "RED")
    finally:
        log_connection(addr, "DISCONNECTED", "RED")
        if username:
            cleanup_user(username)
            print_server_stats()
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
print(f"{colors['GREEN']}{'=' * 60}{colors['RESET']}")
print(f"{colors['GREEN']}           ONLINE PACMAN SERVER STARTED{colors['RESET']}")
print(f"{colors['GREEN']}{'=' * 60}{colors['RESET']}")
print(f"{colors['YELLOW']}Server listening on: {colors['BOLD']}{host}:{port}{colors['RESET']}")
print(f"{colors['YELLOW']}Databases: {colors['RESET']}")
print(f"  Users: {colors['GREY']}{users_db_path}{colors['RESET']}")
print(f"  Lobbies: {colors['GREY']}{lobbies_db_path}{colors['RESET']}")
print(f"{colors['GREEN']}{'=' * 60}{colors['RESET']}")
print(f"{colors['BLUE']}Waiting for connections...{colors['RESET']}\n")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
