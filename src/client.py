import csv
from socket import AF_INET, SOCK_STREAM, socket
from sys import argv

from menus import logInMenu, start_menu
from utils import args, colors, create_db, print_center
from utils import send_client as send


def affiche(map, PacmanPowered):
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


username = ""
password = ""

cache_path = create_db("password_cache.csv")

with open(cache_path, mode="r") as file:
    for row in csv.reader(file):
        username = row[0]
        password = row[1]

if not username or not password:
    username, password = logInMenu()

port, remote_ip = args(argv)

client = socket(AF_INET, SOCK_STREAM)  # IPV4 TCP
try:
    client.connect((remote_ip, port))
except ConnectionRefusedError:
    print(f"{colors['RED']}ERR:{colors['RESET']} Server is offline")
    exit()

send("[USERNAME]:" + username, client)
send("[PASSWORD]:" + password, client)

logged = True

with open(cache_path, mode="w") as file_write:
    csv.writer(file_write).writerow([username, password])

start_menu(logged, client)


#if header == "PACST":
    
#    pacman_state = message
    
#if header == "MAP":

#   map_tmp = message
    
#   affiche(map_tmp, pastate)
#    if kay == 65:
#        send("[MOUV]: avant"
#    if kay == 66:
#        send("[MOUV]: arrière"
#    if kay == 67:
#        send("[MOUV]: droite"
#    if kay == 68:
#        send("[MOUV]: gauche"
