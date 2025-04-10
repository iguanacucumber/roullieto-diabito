from map import tab



x = [1, 18, 10, 11, 13, 12, 9, 14, 15, 16]
y = [7, 0, 17]


def conv(liste):
    convert = liste[:]
    for i in range(len(liste)):
        for j in range(len(liste[i])):
            if liste[i][j] in x:
                convert[i][j] = 1
            elif liste[i][j] in y:
                convert[i][j] = 0

    return convert



print(conv(tab))
