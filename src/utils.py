def args(argv):
    port = 8000
    ip = "127.0.0.1"

    for i in range(len(argv)):
        if argv[i] == "-p" or argv[i] == "--port":
            port = argv[i + 1]
        elif argv[i] == "-i" or argv[i] == "--ip":
            ip = argv[i + 1]
        elif argv[i] == "-h" or argv[i] == "--help":
            print("-i, --ip:   IPV4 IP")
            print("-p, --port: PORT")
            exit()

    return port, ip


def handle_message(msg):
    past_header = False
    inside_brackets = False
    message = ""
    header = ""
    for character in msg:
        if character == "]" and not past_header:
            inside_brackets = False

        if past_header:
            message += character
        elif inside_brackets:
            header += character

        if character == "[" and not past_header:
            inside_brackets = True
        elif character == ":":
            past_header = True

    return message, header


def clear():
    from os import system
    from sys import platform

    if platform.startswith("win"):
        system("cls")
    else:
        system("clear")


colors = {
    "YELLOW": "\033[33m",  # Les couleurs
    "PURPLE": "\033[35m",
    "RED": "\033[91m",
    "GREY": "\033[90m",
    "BLUE": "\033[34m",
    "BOLD": "\033[1m",
    "GREEN": "\033[32m",
    "RESET": "\033[0m",  # Annule la couleur
}
