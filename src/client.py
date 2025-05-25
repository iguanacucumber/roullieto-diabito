import socket
from sys import argv

from utils import args, colors, handle_message


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


def ConnectToALobby():
    import json

    if header == "MAP":
        game_map = json.loads(message)  # Converts from json to a python list
        print(game_map)


def affiche(map, PacmanPowered):  # Pour faire jolie
    nombre = 0
    longueur = int(len(map))
    print("╭", end="")
    print("─" * int(longueur * 2 - 5), end="")
    print("╮", end="")
    print()
    for ligne in map:
        nombre += 1
        print("│ ", end="")
        for case in ligne:
            if case == 0:
                print(f"{colors['GREY']}·{colors['RESET']}", end=" ")

            elif case == 1:
                print(f"{colors['BLUE']}8{colors['RESET']}", end=" ")
            elif case == 2:
                if PacmanPowered:
                    print(f"{colors['BOLD']}ᗤ{colors['RESET']}", end=" ")
                else:
                    print(f"{colors['YELLOW']}ᗤ{colors['RESET']}", end=" ")

            elif case == 3:
                print(f"{colors['RED']}ᗣ{colors['RESET']}", end=" ")
            elif case == 4:
                print(f"{colors['PURPLE']}ᗣ{colors['RESET']}", end=" ")
            elif case == 5:
                print(f"{colors['GREEN']}ᗣ{colors['RESET']}", end=" ")
            elif case == 6:
                print(f"{colors['YELLOW']}⬤{colors['RESET']}", end=" ")
            else:
                print("  ", end="")
        print("│", end="")
        print()

    print("╰", end="")
    print("─" * int(longueur * 2 - 5), end="")
    print("╯")
    print(f"\n{colors['BOLD']}SHIFT + Q{colors['RESET']}: Exit, {colors['BOLD']}Movement{colors['RESET']}: ZQSD or Arrow keys")

    print("\n")


def ClientGame():
    pass


port, remote_ip = args(argv)

while True:
    # clear()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4 TCP
    client.connect((remote_ip, port))

    print((remote_ip, port))
    print("Login if user exists, automatically signs you up otherwise\n")
    global header  # Make those variables available out of this scope
    global message  # Make them available in everywhere in this file
    response = send("[USERNAME]:" + input("Username: "))
    message, header = handle_message(response)
    if header == "OK":
        print(send("[PASSWORD]:" + input("Password: ")))
        if header == "OK":
            pass
        elif header == "MAP":
            affiche(message, False)

    if ConnectToALobby():
        ClientGame()
