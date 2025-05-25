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
