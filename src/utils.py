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


def print_center(text):
    import re
    from os import get_terminal_size

    terminal_size = get_terminal_size()
    terminal_width = terminal_size[0]
    ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")  # Sans ça certains texte ne sont pas centrées
    visible_text = ansi_escape.sub("", text)
    input_length = len(visible_text)
    empty_space_required = (terminal_width - input_length) // 2
    empty_space = " " * empty_space_required
    print(empty_space + text)


def UserInput():
    from sys import platform

    windows = platform.startswith("win")

    if windows:
        import msvcrt

        if msvcrt.kbhit():
            return ord(msvcrt.getch())
    else:
        from sys import stdin
        from termios import TCSADRAIN, tcgetattr, tcsetattr
        from tty import setraw

        fd = stdin.fileno()  # Ouvre un buffer/tty/terminal
        old_settings = tcgetattr(fd)  # Prend les paramètres du buffer/tty
        try:
            setraw(  # Ne print pas les charactères écrits, pas besoin de <enter>
                stdin.fileno()
            )
            return ord(stdin.read(1))  # Lis 1 seule charactère
        finally:
            tcsetattr(  # Définis les paramètres du tty/buffer
                fd, TCSADRAIN, old_settings
            )


def create_db(file_name):
    import os
    from platform import system

    if system() == "Windows":
        base_folder = os.getenv("APPDATA")
    else:  # Linux
        base_folder = os.path.expanduser("~/.local/share")

    full_path = os.path.join(base_folder, "online-pacman")
    os.makedirs(full_path, exist_ok=True)

    db_path = os.path.join(full_path, file_name)

    if not os.path.exists(db_path):  # Crée la db si elle n'existe pas
        with open(db_path, "w") as _:
            pass

    return db_path


def send_client(msg, client):
    message = msg.strip().encode("utf-8")
    msg_length = len(message)
    send_length = str(msg_length).encode("utf-8")
    send_length += b" " * (1024 - len(send_length))
    client.send(send_length)
    client.send(message)
    received_message = client.recv(1024).decode("utf-8")
    message, header = handle_message(received_message)
    if header == "ERR":
        clear()
        print(f"{colors['RED']}ERR:{colors['RESET']} {message}")
        exit()

    return message, header


def db_writerow(end_row, db_path):
    import csv

    length = 0
    pos_user = -1
    db = []

    with open(db_path, mode="r") as file_read:
        for row in csv.reader(file_read):
            db.append(row)
            if row[0] == end_row[0]:
                pos_user = length
            length += 1

    with open(db_path, mode="w") as file_write:
        for row in db:
            if length == pos_user:
                csv.writer(file_write).writerow(end_row)
            else:
                csv.writer(file_write).writerow(row)

            length += 1
        if pos_user == -1:
            csv.writer(file_write).writerow(end_row)

    if pos_user == -1:
        return False  # user does not exist in db
    else:
        return True  # user exists
