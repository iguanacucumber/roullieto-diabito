import os
import random
import time
from msvcrt import getch, kbhit


def affiche(table):
    os.system("cls")
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 1:
                print("║", end="")
            if table[i][j] == 10:
                print("╗", end="")
            if table[i][j] == 7:
                print("░", end="")
            if table[i][j] == 11:
                print("╔", end="")
            if table[i][j] == 13:
                print("═", end="")
            if table[i][j] == 12:
                print("╝", end="")
            if table[i][j] == 9:
                print("╚", end="")
            if table[i][j] == 14:
                print("╣", end="")
            if table[i][j] == 15:
                print("╠", end="")
            if table[i][j] == 16:
                print("╦", end="")
            if table[i][j] == 2:
                print("\1", end="")
            if table[i][j] == 0:
                print("·", end="")
            if table[i][j] == 17:
                print(" ", end="")
            if table[i][j] == 6:
                print("A", end="")
            if table[i][j] == 3:
                print("B", end="")
        print()


def fantome2(lc, cc, lf2, cf2):
    global memo1

    if lc > lf2 and (tab[lf2 + 1][cf2] == 0 or tab[lf2 + 1][cf2] == 17 or tab[lf2 + 1][cf2] == 2):
        if memo1 == 0:
            tab[lf2][cf2] = 0
        if memo1 == 17:
            tab[lf2][cf2] = 17

        lf2 = lf2 + 1
        memo = tab[lf2][cf2]
        tab[lf2][cf2] = 3

    elif lc < lf2 and (tab[lf2 - 1][cf2] == 0 or tab[lf2 - 1][cf2] == 17 or tab[lf2 - 1][cf2] == 2):
        if memo1 == 0:
            tab[lf2][cf2] = 0
        if memo1 == 17:
            tab[lf2][cf2] = 17

        lf2 = lf2 - 1
        memo1 = tab[lf2][cf2]
        tab[lf2][cf2] = 3

    if cc > cf2 and (tab[lf2][cf2 + 1] == 0 or tab[lf2][cf2 + 1] == 17 or tab[lf2][cf2 + 1] == 2):
        if memo1 == 0:
            tab[lf2][cf2] = 0
        if memo1 == 17:
            tab[lf2][cf2] = 17

        cf2 = cf2 + 1
        memo1 = tab[lf2][cf2]
        tab[lf2][cf2] = 3

    elif cc < cf2 and (tab[lf2][cf2 - 1] == 0 or tab[lf2][cf2 - 1] == 17 or tab[lf2][cf2 - 1] == 2):
        if memo1 == 0:
            tab[lf2][cf2] = 0
        if memo1 == 17:
            tab[lf2][cf2] = 17

        cf2 = cf2 - 1
        memo1 = tab[lf2][cf2]
        tab[lf2][cf2] = 3
    return lf2, cf2


def fantome1(l, c, lf1, cf1):
    global memo

    if l > lf1 and (tab[lf1 + 1][cf1] == 0 or tab[lf1 + 1][cf1] == 17 or tab[lf1 + 1][cf1] == 2):
        if memo == 0:
            tab[lf1][cf1] = 0
        if memo == 17:
            tab[lf1][cf1] = 17

        lf1 = lf1 + 1
        memo = tab[lf1][cf1]
        tab[lf1][cf1] = 6

    elif l < lf1 and (tab[lf1 - 1][cf1] == 0 or tab[lf1 - 1][cf1] == 17 or tab[lf1 - 1][cf1] == 2):
        if memo == 0:
            tab[lf1][cf1] = 0
        if memo == 17:
            tab[lf1][cf1] = 17

        lf1 = lf1 - 1
        memo = tab[lf1][cf1]
        tab[lf1][cf1] = 6

    if c > cf1 and (tab[lf1][cf1 + 1] == 0 or tab[lf1][cf1 + 1] == 17 or tab[lf1][cf1 + 1] == 2):
        if memo == 0:
            tab[lf1][cf1] = 0
        if memo == 17:
            tab[lf1][cf1] = 17

        cf1 = cf1 + 1
        memo = tab[lf1][cf1]
        tab[lf1][cf1] = 6
    elif c < cf1 and (tab[lf1][cf1 - 1] == 0 or tab[lf1][cf1 - 1] == 17 or tab[lf1][cf1 - 1] == 2):
        if memo == 0:
            tab[lf1][cf1] = 0
        if memo == 17:
            tab[lf1][cf1] = 17

        cf1 = cf1 - 1
        memo = tab[lf1][cf1]
        tab[lf1][cf1] = 6
    return lf1, cf1


"""def RIP(table):
	if table[lf,cf] == table [l,c]:
	"""

tab = [
    [11, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 16, 16, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 10],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 11, 13, 13, 10, 0, 11, 13, 13, 13, 10, 0, 1, 1, 0, 11, 13, 13, 13, 10, 0, 11, 13, 13, 10, 0, 1],
    [1, 0, 1, 7, 7, 1, 0, 9, 13, 13, 13, 12, 0, 1, 1, 0, 9, 13, 13, 13, 12, 0, 1, 7, 7, 1, 0, 1],
    [1, 0, 9, 13, 13, 12, 0, 0, 0, 0, 0, 0, 0, 9, 12, 0, 0, 0, 0, 0, 0, 0, 9, 13, 13, 12, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 11, 13, 13, 10, 0, 11, 10, 0, 11, 13, 13, 13, 13, 13, 13, 10, 0, 11, 10, 0, 11, 13, 13, 10, 0, 1],
    [1, 0, 9, 13, 13, 12, 0, 1, 1, 0, 9, 13, 13, 16, 16, 13, 13, 12, 0, 1, 1, 0, 9, 13, 13, 12, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [15, 13, 13, 13, 13, 10, 0, 1, 15, 13, 13, 10, 0, 1, 1, 0, 11, 13, 13, 14, 1, 0, 11, 13, 13, 13, 13, 14],
    [1, 7, 7, 7, 7, 1, 0, 1, 15, 13, 13, 12, 0, 9, 12, 0, 9, 13, 13, 14, 1, 0, 1, 7, 7, 7, 7, 1],
    [1, 7, 7, 7, 7, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 7, 7, 7, 7, 1],
    [1, 7, 7, 7, 7, 1, 0, 1, 1, 0, 11, 13, 13, 17, 17, 13, 13, 10, 0, 1, 1, 0, 1, 7, 7, 7, 7, 1],
    [15, 13, 13, 13, 13, 12, 0, 9, 12, 0, 1, 17, 17, 17, 17, 17, 17, 1, 0, 9, 12, 0, 9, 13, 13, 13, 13, 14],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 17, 17, 6, 3, 17, 17, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [15, 13, 13, 13, 13, 10, 0, 11, 10, 0, 1, 17, 17, 17, 17, 17, 17, 1, 0, 11, 10, 0, 11, 13, 13, 13, 13, 14],
    [1, 7, 7, 7, 7, 1, 0, 1, 1, 0, 9, 13, 13, 13, 13, 13, 13, 12, 0, 1, 1, 0, 1, 7, 7, 7, 7, 1],
    [1, 7, 7, 7, 7, 1, 0, 1, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 0, 1, 7, 7, 7, 7, 1],
    [1, 7, 7, 7, 7, 1, 0, 1, 1, 0, 11, 13, 13, 13, 13, 13, 13, 10, 0, 1, 1, 0, 1, 7, 7, 7, 7, 1],
    [15, 13, 13, 13, 13, 12, 0, 9, 12, 0, 9, 13, 13, 16, 16, 13, 13, 12, 0, 9, 12, 0, 9, 13, 13, 13, 13, 14],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 11, 13, 13, 10, 0, 11, 13, 13, 13, 10, 0, 1, 1, 0, 11, 13, 13, 13, 10, 0, 11, 13, 13, 10, 0, 1],
    [1, 0, 9, 13, 10, 1, 0, 9, 13, 13, 13, 12, 0, 9, 12, 0, 9, 13, 13, 13, 12, 0, 1, 11, 13, 12, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [15, 13, 10, 0, 1, 1, 0, 11, 10, 0, 11, 13, 13, 13, 13, 13, 13, 10, 0, 11, 10, 0, 1, 1, 0, 11, 13, 14],
    [15, 13, 12, 0, 9, 12, 0, 1, 1, 0, 9, 13, 13, 10, 11, 13, 13, 12, 0, 1, 1, 0, 9, 12, 0, 9, 13, 14],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 11, 13, 13, 13, 13, 12, 9, 13, 13, 10, 0, 1, 1, 0, 11, 13, 13, 12, 9, 13, 13, 13, 13, 10, 0, 1],
    [1, 0, 9, 13, 13, 13, 13, 13, 13, 13, 13, 12, 0, 9, 12, 0, 9, 13, 13, 13, 13, 13, 13, 13, 13, 12, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [9, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12],
]
affiche(tab)
ligne = 20
colonne = 25

lc = random.randint(1, 28)
cc = random.randint(1, 26)


l = 17
c = 13

lf2 = 14
cf2 = 14

lf1 = 14
cf1 = 13

compteur1 = 0
compteur2 = 0
compteur3 = 0

memo = 17  # ya un point sinon 17 pour espace
memo1 = 17
score = 0
while True:
    if kbhit():
        z = getch()  # lecture touche
        code = ord(z)  # code ASCII
        """print (code)"""

        # haut
        if code == 122:
            if tab[l - 1][c] == 0:
                tab[l][c] = 17
                l = l - 1
                tab[l][c] = 2
                affiche(tab)
                score = score + 1
                print(score)
            if tab[l - 1][c] == 17:
                tab[l][c] = 17
                l = l - 1
                tab[l][c] = 2
                affiche(tab)
                print(score)
        # gauche
        if code == 113:
            if tab[l][c - 1] == 0:
                tab[l][c] = 17
                c = c - 1
                tab[l][c] = 2
                affiche(tab)
                score = score + 1
                print(score)
            if tab[l][c - 1] == 17:
                tab[l][c] = 17
                c = c - 1
                tab[l][c] = 2
                affiche(tab)
                print(score)
        # bas
        if code == 115:
            if tab[l + 1][c] == 0:
                tab[l][c] = 17
                l = l + 1
                tab[l][c] = 2
                affiche(tab)
                score = score + 1
                print(score)

            if tab[l + 1][c] == 17:
                tab[l][c] = 17
                l = l + 1
                tab[l][c] = 2
                affiche(tab)
                print(score)
        # droite
        if code == 100:
            if tab[l][c + 1] == 0:
                tab[l][c] = 17
                c = c + 1
                tab[l][c] = 2
                affiche(tab)
                score = score + 1
                print(score)

            if tab[l][c + 1] == 17:
                tab[l][c] = 17
                c = c + 1
                tab[l][c] = 2
                affiche(tab)
                print(score)

    if score == 500:
        os.system("cls")
        print("you're GAY")
    compteur1 = compteur1 + 1
    compteur2 = compteur2 + 1
    compteur3 = compteur3 + 1
    if compteur1 > 10:
        lf1, cf1 = fantome1(l, c, lf1, cf1)
        affiche(tab)
        compteur1 = 0
    if compteur2 > 10:
        lf2, cf2 = fantome2(lc, cc, lf2, cf2)
        affiche(tab)
        compteur2 = 0
    if compteur3 > 100:
        lc = random.randint(1, 28)
        cc = random.randint(1, 26)
        compteur3 = 0
    time.sleep(0.01)
