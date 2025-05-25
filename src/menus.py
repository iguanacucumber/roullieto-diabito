import re
from os import get_terminal_size

from utils import UserInput, clear, colors, print_center
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

    size = get_terminal_size()  # Print the menu in the center of the screen
    height = size.lines
    width = size.columns

    total_items = len(items)
    start_row = (height // 2) - (total_items // 2)

    for i in range(total_items):
        if i == selected:
            label = f"▶ {colors['YELLOW']}{items[i]}{colors['RESET']}"
        else:
            label = f"{colors['BLUE']}{items[i]}{colors['RESET']}"
        visible_length = len(re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", label))  # Removes any colors / formatting to get the true length of the string
        col = (width - visible_length) // 2
        print(f"\033[{start_row + i};{col}H{label}")

    height = get_terminal_size().lines  # Move the cursor to the bottom
    print(f"\033[{height};1H", end="")
    print_center("Use ↑ ↓ to move, Enter to select an option")


def lobbyMenu():
    selected = 0
    lobby_items = []  # TODO: get lobbies from server

    draw_menu(lobby_items, selected)


def logInMenu():
    pass
    # create_db("password_cache.csv")


def start_menu(logged, client):
    selected = 0
    start_menu_items = [
        "Lobbies ",
        "Log Out ",
        "Exit    ",
    ]

    while True:
        if not logged:
            logInMenu()

        draw_menu(start_menu_items, selected)

        input = UserInput()

        if input == 66:
            selected += 1
        elif input == 65:
            selected -= 1
        elif input == 13:
            if selected == 0:
                pass
                lobbyMenu()
            if selected == 1:
                logInMenu()
            if selected == 2:
                clear()
                send("[DISCONNECT]:", client)
                exit()

        if selected < 0:
            selected = 0
        elif selected > 2:
            selected = 2
