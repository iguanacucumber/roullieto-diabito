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
