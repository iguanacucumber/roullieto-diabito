# Ce code est l'ancien code pacman est n'est activement utilisé

import random
from os import system
from sys import platform
from time import sleep

windows = platform.startswith("win")

if windows:
    import msvcrt
else:
    import sys
    import termios
    import tty


# fonction
def affiche_refresh(fps):
    clear()
    affiche()
    sleep(1 / fps)


def clear():
    if windows:
        system("cls")
    else:
        system("clear")


YELLOW = "\033[33m"  # Les couleurs
PURPLE = "\033[35m"
RED = "\033[91m"
GREY = "\033[90m"
BLUE = "\033[34m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RESET = "\033[0m"  # Annule la couleur

PacmanPowered = False


def locatePacman():
    for i in range(len(jeu)):
        for j in range(len(jeu[0])):
            if jeu[i][j] == 2:
                return j, i  # x, y
    return False


def locateFantomes():  # localiser un fantomes pour tuer pacman
    fantomes = []
    for i in range(len(jeu)):
        for j in range(len(jeu[0])):
            if jeu[i][j] == 3 or jeu[i][j] == 4 or jeu[i][j] == 5:
                fantomes.append([i, j])  # y, x

    return fantomes


def locatefantome(p):  # localiser un fantomes particulier
    for i in range(len(jeu)):
        for j in range(len(jeu[0])):
            if jeu[i][j] == p:
                return j, i  # x, y
    return -1, -1  # Not found


def pacmanMouvement(pacmanPosX, pacmanPosY, a, b):
    global PacmanPowered
    if jeu[pacmanPosY + b][pacmanPosX + a] == 0:
        jeu[pacmanPosY + b][pacmanPosX + a] = 2
        jeu[pacmanPosY][pacmanPosX] = 0
    elif (
        jeu[pacmanPosY + b][pacmanPosX + a] == 3 or jeu[pacmanPosY + b][pacmanPosX + a] == 4 or jeu[pacmanPosY + b][pacmanPosX + a] == 5
    ) and not PacmanPowered:
        jeu[pacmanPosY][pacmanPosX] = jeu[pacmanPosY + b][pacmanPosX + a]
    elif (jeu[pacmanPosY + b][pacmanPosX + a] == 3 or jeu[pacmanPosY + b][pacmanPosX + a] == 4 or jeu[pacmanPosY + b][pacmanPosX + a] == 5) and PacmanPowered:
        jeu[pacmanPosY + b][pacmanPosX + a] = 2
        jeu[pacmanPosY + b][pacmanPosX + a] = 0
    elif jeu[pacmanPosY + b][pacmanPosX + a] == 6:
        jeu[pacmanPosY + b][pacmanPosX + a] = 0
        PacmanPowered = True


def fantomeMouvement(fantomesPosX, fantomesPosY, a, b, fantome):
    if jeu[fantomesPosY + b][fantomesPosX + a] == 0 or jeu[fantomesPosY + b][fantomesPosX + a] == 2:
        jeu[fantomesPosY + b][fantomesPosX + a] = fantome
        jeu[fantomesPosY][fantomesPosX] = 0


def fantomekill():  # le truc pour tuer le pacman
    global PacmanPowered
    fantomes = locateFantomes()

    if len(fantomes) == 0:
        return True

    for fantome in fantomes:
        if jeu[fantome[0]][fantome[1]] == 2 and not PacmanPowered:
            return False

        elif jeu[fantome[0]][fantome[1]] == 2 and PacmanPowered:
            return None


def affiche():  # Pour faire jolie
    nombre = 0
    longueur = int(len(jeu))
    print("╭", end="")
    print("─" * int(longueur * 2 + 5), end="")
    print("╮", end="")
    print()
    for ligne in jeu:
        nombre += 1
        print("│ ", end="")
        for case in ligne:
            if case == 0:
                print(f"{GREY}·{RESET}", end=" ")
            elif case == 1:
                print(f"{BLUE}8{RESET}", end=" ")
            elif case == 2:
                if PacmanPowered:
                    print(f"{BOLD}ᗤ{RESET}", end=" ")
                else:
                    print(f"{YELLOW}ᗤ{RESET}", end=" ")

            elif case == 3:
                print(f"{RED}ᗣ{RESET}", end=" ")
            elif case == 4:
                print(f"{PURPLE}ᗣ{RESET}", end=" ")
            elif case == 5:
                print(f"{GREEN}ᗣ{RESET}", end=" ")
            elif case == 6:
                print(f"{YELLOW}⬤{RESET}", end=" ")
            else:
                print("  ", end="")
        print("│", end="")
        print()

    print("╰", end="")
    print("─" * int(longueur * 2 + 5), end="")
    print("╯")
    print(f"\n{BOLD}SHIFT + Q{RESET}: Exit, {BOLD}Movement{RESET}: ZQSD or Arrow keys")

    print("\n")


def UserInputGame(code):
    if not locatePacman():
        return

    pacmanPosX, pacmanPosY = locatePacman()

    if code == 122:  # z, up arrow
        pacmanMouvement(pacmanPosX, pacmanPosY, 0, -1)
    elif code == 113:  # q, left arrow
        pacmanMouvement(pacmanPosX, pacmanPosY, -1, 0)
    elif code == 115:  # s, down arrow
        pacmanMouvement(pacmanPosX, pacmanPosY, 0, 1)
    elif code == 100:  # d, right arrow
        pacmanMouvement(pacmanPosX, pacmanPosY, 1, 0)
    elif code == 81:  # Q
        clear()
        print("Quit le jeu")
        exit()


def IArandom(fantome):
    if not locatePacman():
        return

    fantomeX, fantomeY = locatefantome(fantome)

    if fantomeX == -1 and fantomeY == -1:
        return

    while True:
        mouvement = random.randint(1, 4)
        if mouvement == 1 and jeu[fantomeY - 1][fantomeX] != 1:  # haut
            fantomeMouvement(fantomeX, fantomeY, 0, -1, fantome)
            return
        elif mouvement == 2 and jeu[fantomeY + 1][fantomeX] != 1:  # bas
            fantomeMouvement(fantomeX, fantomeY, 0, 1, fantome)
            return
        elif mouvement == 3 and jeu[fantomeY][fantomeX - 1] != 1:  # gauche
            fantomeMouvement(fantomeX, fantomeY, -1, 0, fantome)
            return
        elif mouvement == 4 and jeu[fantomeY][fantomeX + 1] != 1:  # droit
            fantomeMouvement(fantomeX, fantomeY, 1, 0, fantome)
            return


def IAPointRandom(fantome, coorX, coorY):
    if not locatePacman():
        return

    fantomeX, fantomeY = locatefantome(fantome)

    if fantomeX == -1 and fantomeY == -1:
        return

    if randomCoorX > fantomeX and jeu[fantomeY][fantomeX + 1] != 1:
        fantomeMouvement(fantomeX, fantomeY, 1, 0, fantome)
        return
    elif randomCoorX < fantomeX and jeu[fantomeY][fantomeX - 1] != 1:
        fantomeMouvement(fantomeX, fantomeY, -1, 0, fantome)
        return
    elif randomCoorY > fantomeY and jeu[fantomeY + 1][fantomeX] != 1:
        fantomeMouvement(fantomeX, fantomeY, 0, 1, fantome)
        return
    elif randomCoorY < fantomeY and jeu[fantomeY - 1][fantomeX] != 1:
        fantomeMouvement(fantomeX, fantomeY, 0, -1, fantome)
        return
    else:
        IArandom(fantome)


def IAInteligent():
    if not locatePacman():
        return

    pacmanX, pacmanY = locatePacman()

    fantomeX, fantomeY = locatefantome(3)

    if pacmanX > fantomeX and jeu[fantomeY][fantomeX + 1] != 1:
        fantomeMouvement(fantomeX, fantomeY, 1, 0, 3)
        return
    elif pacmanX < fantomeX and jeu[fantomeY][fantomeX - 1] != 1:
        fantomeMouvement(fantomeX, fantomeY, -1, 0, 3)
        return
    elif pacmanY > fantomeY and jeu[fantomeY + 1][fantomeX] != 1:
        fantomeMouvement(fantomeX, fantomeY, 0, 1, 3)
        return
    elif pacmanY < fantomeY and jeu[fantomeY - 1][fantomeX] != 1:
        fantomeMouvement(fantomeX, fantomeY, 0, -1, 3)
        return
    else:
        IArandom(3)


def userInputUnix():
    global code
    fd = sys.stdin.fileno()  # Ouvre un buffer/tty/terminal
    old_settings = termios.tcgetattr(fd)  # Prend les paramètres du buffer/tty
    try:
        tty.setraw(  # Ne print pas les charactères écrits, pas besoin de <enter>
            sys.stdin.fileno()
        )
        character = ord(sys.stdin.read(1))  # Lis 1 seule charactère
    finally:
        termios.tcsetattr(  # Définis les paramètres du tty/buffer
            fd, termios.TCSADRAIN, old_settings
        )

    if character:
        return UserInputGame(character)
    else:
        return code


def UserInputWindows():
    global code
    if msvcrt.kbhit():
        character = msvcrt.getch()
        if character:
            return ord(character)
        else:
            return code


jeu = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 6, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 6, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

PacmanPowered = False
PoweredFrames = 0
frames = 0
randomCoorX = random.randint(0, len(jeu) - 1)
randomCoorY = random.randint(0, len(jeu[0]) - 1)

while True:
    affiche_refresh(fps=16)
    if windows:
        code = UserInputWindows()
    else:
        code = userInputUnix()

    if PacmanPowered:
        PoweredFrames += 1
        if PoweredFrames == 80:  # Powerup dure 5s
            PoweredFrames = 0
            PacmanPowered = False

    fantomeX5, fantomeY5 = locatefantome(5)
    if frames % 160 or (fantomeX5 == randomCoorX and fantomeY5 == randomCoorY):
        while True:
            randomCoorX = random.randint(0, len(jeu) - 1)
            randomCoorY = random.randint(0, len(jeu[0]) - 1)
            if jeu[randomCoorY][randomCoorX] == 0:
                break

    if frames % 2 == 0:
        UserInputGame(code)
        IAInteligent()  # Execute l'IA du fantome 3
        IAPointRandom(5, randomCoorX, randomCoorY)  # Execute l'IA du fantome 5

    IArandom(4)  # Execute l'IA du fantome 4

    win = fantomekill()
    if win:
        clear()
        print(f"""{YELLOW}
__   __           __        __
\ \ / /__  _   _  \ \      / / (_)____
 \ V / _ \| | | |  \ \ /\ / /  | |  _ \ 
  | | (_) | |_| |   \ V  V /   | | | | |
  |_|\___/ \____|    \_/\_/    |_|_| |_|
{RESET}""")
        exit()

    elif win == False or not locatePacman():
        clear()
        print(f"""{RED}
▄██   ▄    ▄██████▄  ███    █▄       ████████▄   ▄█     ▄████████ ████████▄
███   ██▄ ███    ███ ███    ███      ███   ▀███ ███    ███    ███ ███   ▀███
███▄▄▄███ ███    ███ ███    ███      ███    ███ ███▌   ███    █▀  ███    ███
▀▀▀▀▀▀███ ███    ███ ███    ███      ███    ███ ███▌  ▄███▄▄▄     ███    ███
▄██   ███ ███    ███ ███    ███      ███    ███ ███▌ ▀▀███▀▀▀     ███    ███
███   ███ ███    ███ ███    ███      ███    ███ ███    ███    █▄  ███    ███
███   ███ ███    ███ ███    ███      ███   ▄███ ███    ███    ███ ███    ███
 ▀█████▀   ▀██████▀  ████████▀       ████████▀  █▀     ██████████ ████████▀
{RESET}""")
        exit()
    elif win == None:
        pass
