import csv
import json
import re
from os import get_terminal_size

from utils import UserInput, clear, colors, create_db, print_center , handle_message
from utils import send_client as send

def affiche(map, PacmanPowered):
    draw_menu
    nombre = 0
    longueur = int(len(map))
    up_border = "╭" + "─" * int(longueur * 2 - 5) + "╮"
    print_center(up_border)
    for ligne in map:
        nombre += 1
        line = "│ "
        for case in ligne:
            if case == 0:
                line += f"{colors['GREY']}·{colors['RESET']} "
            elif case == 1:
                line += f"{colors['BLUE']}8{colors['RESET']} "
            elif case == 2:
                if PacmanPowered:
                    line += f"{colors['BOLD']}ᗤ{colors['RESET']} "
                else:
                    line += f"{colors['YELLOW']}ᗤ{colors['RESET']} "
            elif case == 3:
                line += f"{colors['RED']}ᗣ{colors['RESET']} "
            elif case == 4:
                line += f"{colors['PURPLE']}ᗣ{colors['RESET']} "
            elif case == 5:
                line += f"{colors['GREEN']}ᗣ{colors['RESET']} "
            elif case == 6:
                line += f"{colors['YELLOW']}⬤{colors['RESET']} "
            else:
                line += "  "
        line += "│"
        print_center(line)

    down_border = "╰" + "─" * int(longueur * 2 - 5) + "╯"
    print_center(down_border)
    print()
    print_center(f"{colors['BOLD']}SHIFT + Q{colors['RESET']}: Exit, {colors['BOLD']}Movement{colors['RESET']}: ZQSD or Arrow keys")

def draw_menu():
    clear()
    print("\n")

    banner = f"""    ██████╗ ███╗   ██╗██╗     ██╗███╗   ██╗███████╗  {colors["YELLOW"]}██████╗  █████╗  ██████╗███╗   ███╗ █████╗ ███╗   ██╗{colors["RESET"]}
    ██╔═══██╗████╗  ██║██║     ██║████╗  ██║██╔════╝  {colors["YELLOW"]}██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔══██╗████╗  ██║{colors["RESET"]}
    ██║   ██║██╔██╗ ██║██║     ██║██╔██╗ ██║█████╗    {colors["YELLOW"]}██████╔╝███████║██║     ██╔████╔██║███████║██╔██╗ ██║{colors["RESET"]}
    ██║   ██║██║╚██╗██║██║     ██║██║╚██╗██║██╔══╝    {colors["YELLOW"]}██╔═══╝ ██╔══██║██║     ██║╚██╔╝██║██╔══██║██║╚██╗██║{colors["RESET"]}
    ╚██████╔╝██║ ╚████║███████╗██║██║ ╚████║███████╗  {colors["YELLOW"]}██║     ██║  ██║╚██████╗██║ ╚═╝ ██║██║  ██║██║ ╚████║{colors["RESET"]}
    ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝  {colors["YELLOW"]}╚═╝     ╚═╝  ╚═╝ ╚═════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝{colors["RESET"]}"""



while True:
    message, header = handle_message()
    if header == "[MAP]" :
        affiche(message, False)
        key = UserInput()
        if key == 65:
            send("[MOUV]: avant")
        if key == 66:
            send("[MOUV]: arrière")
        if key == 67:
            send("[MOUV]: droite")
        if key == 68:
            send("[MOUV]: gauche")
    elif header == "[]"
        