import re
from os import get_terminal_size

from utils import UserInput, clear, colors, print_center


def menu():
    selected = 0
    menu_item = [
        "Lobbies ",
        "Skins   ",
        "Settings",
        "Exit    ",
    ]
    while True:
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

        total_items = len(menu_item)
        start_row = (height // 2) - (total_items // 2)

        for i in range(total_items):
            if i == selected:
                label = f"▶ {colors['YELLOW']}{menu_item[i]}{colors['RESET']}"
            else:
                label = f"{colors['BLUE']}{menu_item[i]}{colors['RESET']}"
            visible_length = len(re.sub(r"\x1B\[[0-?]*[ -/]*[@-~]", "", label))  # Removes any colors / formatting to get the true length of the string
            col = (width - visible_length) // 2
            print(f"\033[{start_row + i};{col}H{label}")

        height = get_terminal_size().lines  # Move the cursor to the bottom
        print(f"\033[{height};1H", end="")
        print_center("Use ↑ ↓ to move, Enter to select an option")

        if UserInput() == 66:
            selected += 1
        elif UserInput() == 65:
            selected -= 1

        if selected < 0:
            selected = 0
        elif selected > 3:
            selected = 3
