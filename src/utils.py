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
        if character == "]":
            inside_brackets = False

        if past_header:
            message += character
        elif inside_brackets:
            header += character

        if character == "[":
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
