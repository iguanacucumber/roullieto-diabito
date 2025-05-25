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
        print_center(f"{colors['GREEN']}Lobby created successfully!{colors['RESET']}")
        print_center(f"{colors['BLUE']}Lobby ID: {message}{colors['RESET']}")
        print_center("Press Enter to continue...")
        input()
        return True
    else:
        print_center(f"{colors['RED']}Failed to create lobby{colors['RESET']}")
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
                    print_center(f"{colors['GREEN']}Joined lobby successfully!{colors['RESET']}")
                    print_center("Press Enter to continue...")
                    input()
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
                logged = False
            if selected == 2:
                clear()
                exit()

        if selected < 0:
            selected = 0
        elif selected > 2:
            selected = 2
