import csv
import json
import re
from os import get_terminal_size

from utils import UserInput, clear, colors, create_db, print_center
from utils import send_client as send


def draw_menu(items, selected):
    clear()
    print("\n")

    banner = f"""    ██████╗ ███╗   ██╗██╗     ██╗███╗   ██╗███████╗  {colors["YELLOW"]}██████╗  █████╗  ██████╗███╗   ███╗ █████╗ ███╗   ██╗{colors["RESET"]}
    ██╔═══██╗████╗  ██║██║     ██║████╗  ██║██╔════╝  {colors["YELLOW"]}██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔══██╗████╗  ██║{colors["RESET"]}
    ██║   ██║██╔██╗ ██║██║     ██║██╔██╗ ██║█████╗    {colors["YELLOW"]}██████╔╝███████║██║     ██╔████╔██║███████║██╔██╗ ██║{colors["RESET"]}
    ██║   ██║██║╚██╗██║██║     ██║██║╚██╗██║██╔══╝    {colors["YELLOW"]}██╔═══╝ ██╔══██║██║     ██║╚██╔╝██║██╔══██║██║╚██╗██║{colors["RESET"]}
    ╚██████╔╝██║ ╚████║███████╗██║██║ ╚████║███████╗  {colors["YELLOW"]}██║     ██║  ██║╚██████╗██║ ╚═╝ ██║██║  ██║██║ ╚████║{colors["RESET"]}
    ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝  {colors["YELLOW"]}╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝{colors["RESET"]}"""

    for line in banner.splitlines():
        print_center(line)

    print("\n\n\n\n\n")

    size = get_terminal_size()
    height = size.lines
    width = size.columns

    total_items = len(items)
    start_row = (height // 2) - (total_items // 2)

    for i in range(total_items):
        if i == selected:
            label = f"▶ {colors['YELLOW']}{items[i]}{colors['RESET']}"
        else:
            label = f"{colors['BLUE']}{items[i]}{colors['RESET']}"
        visible_length = len(re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", label))
        col = (width - visible_length) // 2
        print(f"\033[{start_row + i};{col}H{label}")

    height = get_terminal_size().lines
    print(f"\033[{height};1H", end="")
    print_center("Use ↑ ↓ to move, Enter to select an option")


def centered_input(prompt):
    cols = get_terminal_size().columns
    col = (cols - len(prompt)) // 2
    print(" " * col + prompt, end="", flush=True)
    return input()


def draw_lobby_list(lobbies, selected):
    clear()
    print("\n")
    print_center(f"{colors['BOLD']}╭─────────────────────────────────╮{colors['RESET']}")
    print_center(f"{colors['BOLD']}│          LOBBY LIST             │{colors['RESET']}")
    print_center(f"{colors['BOLD']}╰─────────────────────────────────╯{colors['RESET']}")
    print("\n")

    if not lobbies:
        print_center(f"{colors['GREY']}No lobbies available{colors['RESET']}")
        print("\n")
        print_center(
            f"{colors['BLUE']}C{colors['RESET']}: Create Lobby | {colors['BLUE']}R{colors['RESET']}: Refresh | {colors['BLUE']}B{colors['RESET']}: Back"
        )
        return

    for i, lobby in enumerate(lobbies):
        status_color = colors["GREEN"] if lobby["status"] == "waiting" else colors["RED"]
        player_info = f"{lobby['players']}/{lobby['max_players']}"

        if i == selected:
            line = f"▶ {colors['YELLOW']}{lobby['name']:<20}{colors['RESET']} [{status_color}{lobby['status']:<8}{colors['RESET']}] ({player_info})"
        else:
            line = f"  {colors['BLUE']}{lobby['name']:<20}{colors['RESET']} [{status_color}{lobby['status']:<8}{colors['RESET']}] ({player_info})"

        print_center(line)

    print("\n")
    print_center(
        f"{colors['BLUE']}Enter{colors['RESET']}: Join | {colors['BLUE']}C{colors['RESET']}: Create | {colors['BLUE']}R{colors['RESET']}: Refresh | {colors['BLUE']}B{colors['RESET']}: Back"
    )


def draw_lobby_room(lobby_info):
    clear()
    print("\n")
    print_center(f"{colors['BOLD']}╭" + "─" *(len(lobby_info['name']) + 15) + f"╮{colors['RESET']}")
    print_center(f"{colors['BOLD']}│       LOBBY: {lobby_info['name']} │{colors['RESET']}")
    print_center(f"{colors['BOLD']}╰" + "─" *(len(lobby_info['name']) + 15) + f"╯{colors['RESET']}")
    print("\n")

    print_center(f"{colors['BLUE']}Players ({len(lobby_info['players'])}/{lobby_info['max_players']}):{colors['RESET']}")
    print()

    for i, player in enumerate(lobby_info["players"], 1):
        if i == 1:
            print_center(f"{colors['YELLOW']}👑 {player} (Host){colors['RESET']}")
        else:
            print_center(f"{colors['GREEN']}🟢 {player}{colors['RESET']}")

    # Show empty slots
    for i in range(len(lobby_info["players"]), lobby_info["max_players"]):
        print_center(f"{colors['GREY']}⚪ Waiting for player...{colors['RESET']}")

    print("\n")

    if lobby_info["status"] == "waiting":
        if len(lobby_info["players"]) >= 2:
            print_center(f"{colors['GREEN']}Ready to start!{colors['RESET']}")
            print_center(
                f"{colors['BLUE']}S{colors['RESET']}: Start Game | {colors['BLUE']}R{colors['RESET']}: Refresh | {colors['BLUE']}L{colors['RESET']}: Leave"
            )
        else:
            print_center(f"{colors['YELLOW']}Waiting for more players...{colors['RESET']}")
            print_center(f"{colors['BLUE']}R{colors['RESET']}: Refresh | {colors['BLUE']}L{colors['RESET']}: Leave")
    else:
        print_center(f"{colors['RED']}Game in progress...{colors['RESET']}")
        print_center(f"{colors['BLUE']}L{colors['RESET']}: Leave Lobby")


def lobby_room(client, lobby_id):
    while True:
        message, header = send(f"[GET_LOBBY_INFO]:{lobby_id}", client)

        if header == "LOBBY_INFO":
            try:
                lobby_info = json.loads(message)
                draw_lobby_room(lobby_info)
            except:
                print_center(f"{colors['RED']}Error getting lobby info{colors['RESET']}")
                input()
                return False
        elif header == "ERR":
            print_center(f"{colors['RED']}Error: {message}{colors['RESET']}")
            input()
            return False

        key = UserInput()

        if key == 115 or key == 83:  # 's' or 'S' - Start game
            if lobby_info["status"] == "waiting" and len(lobby_info["players"]) >= 2:
                message, header = send(f"[START_GAME]:{lobby_id}", client)
                if header == "GAME_STARTED":
                    print_center(f"{colors['GREEN']}Game started!{colors['RESET']}")
                    print_center("Press Enter to continue...")
                    input()
                    # TODO: Start actual game logic here
                    return True
                else:
                    print_center(f"{colors['RED']}Could not start game: {message}{colors['RESET']}")
                    print_center("Press Enter to continue...")
                    input()
        elif key == 114 or key == 82:  # 'r' or 'R' - Refresh
            continue
        elif key == 108 or key == 76:  # 'l' or 'L' - Leave
            message, header = send(f"[LEAVE_LOBBY]:{lobby_id}", client)
            if header == "OK":
                print_center(f"{colors['GREEN']}Left lobby successfully{colors['RESET']}")
                print_center("Press Enter to continue...")
                input()
            return False


def createLobbyMenu(client):
    clear()
    print("\n\n\n")
    print_center(f"{colors['BOLD']}╭────────────────────╮{colors['RESET']}")
    print_center(f"{colors['BOLD']}│   CREATE LOBBY     │{colors['RESET']}")
    print_center(f"{colors['BOLD']}╰────────────────────╯{colors['RESET']}")
    print()

    print_center(f"{colors['BLUE']}Lobby Name:{colors['RESET']}")
    lobby_name = centered_input("> ").strip()

    if not lobby_name:
        return False

    print_center(f"{colors['BLUE']}Max Players (2-4):{colors['RESET']}")
    try:
        max_players = int(centered_input("> ").strip())
        if max_players < 2 or max_players > 4:
            print_center(f"{colors['RED']}Invalid player count{colors['RESET']}")
            input()
            return False
    except ValueError:
        print_center(f"{colors['RED']}Invalid number{colors['RESET']}")
        input()
        return False

    message, header = send(f"[CREATE_LOBBY]:{lobby_name}:{max_players}", client)

    if header == "LOBBY_CREATED":
        lobby_id = int(message)
        print_center(f"{colors['GREEN']}Lobby created successfully!{colors['RESET']}")
        print_center(f"{colors['BLUE']}Lobby ID: {lobby_id}{colors['RESET']}")
        print_center("Press Enter to continue...")
        input()

        return lobby_room(client, lobby_id)
    else:
        print_center(f"{colors['RED']}Failed to create lobby: {message}{colors['RESET']}")
        input()
        return False


def lobbyMenu(client):
    selected = 0
    lobbies = []

    while True:
        message, header = send("[GET_LOBBIES]:", client)

        if header == "LOBBIES":
            try:
                lobbies = json.loads(message)
            except:
                lobbies = []

        draw_lobby_list(lobbies, selected)

        key = UserInput()

        if key == 66:  # Down arrow
            if lobbies and selected < len(lobbies) - 1:
                selected += 1
        elif key == 65:  # Up arrow
            if selected > 0:
                selected -= 1
        elif key == 13:  # Enter
            if lobbies and selected < len(lobbies):
                lobby_id = lobbies[selected]["id"]
                message, header = send(f"[JOIN_LOBBY]:{lobby_id}", client)

                if header == "LOBBY_JOINED":
                    if lobby_room(client, lobby_id):
                        return True
                else:
                    print_center(f"{colors['RED']}Failed to join lobby: {message}{colors['RESET']}")
                    print_center("Press Enter to continue...")
                    input()
        elif key == 99 or key == 67:  # 'c' or 'C'
            if createLobbyMenu(client):
                return True
        elif key == 114 or key == 82:  # 'r' or 'R'
            continue
        elif key == 98 or key == 66:  # 'b' or 'B'
            return False


def logInMenu():
    for label in ["Username", "Password"]:
        clear()
        print("\n\n\n")
        print_center(f"{colors['BOLD']}╭────────────────╮{colors['RESET']}")
        print_center(f"{colors['BOLD']}│   LOGIN MENU   │{colors['RESET']}")
        print_center(f"{colors['BOLD']}╰────────────────╯{colors['RESET']}")
        print()
        print_center(f"{colors['BLUE']}{label}:{colors['RESET']}")
        if label == "Username":
            username = centered_input("> ").strip()
        else:
            password = centered_input("> ").strip()
    return username, password


def start_menu(logged, client):
    selected = 0
    start_menu_items = [
        "Lobbies ",
        "Log Out ",
        "Exit    ",
    ]

    while True:
        if not logged:
            username, password = logInMenu()
            send("[USERNAME]:" + username, client)
            send("[PASSWORD]:" + password, client)
            logged = True

            cache_path = create_db("password_cache.csv")
            with open(cache_path, mode="w") as file_write:
                csv.writer(file_write).writerow([username, password])

        draw_menu(start_menu_items, selected)

        input_key = UserInput()

        if input_key == 66:
            selected += 1
        elif input_key == 65:
            selected -= 1
        elif input_key == 13:
            if selected == 0:
                lobbyMenu(client)
            if selected == 1:
                clear()
                logged = False
                send("[DISCONNECT]", client)
                cache_path = create_db("password_cache.csv")
                with open(cache_path, mode="w") as file_write:
                    pass
                exit()
            if selected == 2:
                clear()
                send("[DISCONNECT]", client)
                exit()

        if selected < 0:
            selected = 0
        elif selected > 2:
            selected = 2
