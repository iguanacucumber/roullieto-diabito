import socket
from sys import argv

from menu import menu
from utils import args, colors, print_center


def send(msg):
    message = msg.strip().encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b" " * (1024 - len(send_length))
    client.send(send_length)
    client.send(message)
    received_message = client.recv(1024).decode("utf-8")
    print(received_message)
    return received_message


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


def ClientGame():
    pass


while True:
    menu()

    if not menu:
        port, remote_ip = args(argv)

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 TCP
        client.connect((remote_ip, port))

        print((remote_ip, port))
