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


def listtostr(liste):
    lestr = ""
    for i in range(len(liste)):
        lestr += "["
        for j in range(len(liste[i])):
            lestr += str(liste[i][j])
            lestr += ","
        lestr += "]"
    return lestr


def strtolistoflists(s):
    try:
        # ast.literal_eval évalue une chaîne de manière sécurisée
        result = ast.literal_eval(s)
        if isinstance(result, list) and all(isinstance(sublist, list) for sublist in result):
            return result
        else:
            raise ValueError("La chaîne ne représente pas une liste de listes.")
    except Exception as e:
        print(f"Erreur lors de la conversion : {e}")
        return None


laliste = [[1, 2], [1, 5]]
print(listtostr(laliste))
