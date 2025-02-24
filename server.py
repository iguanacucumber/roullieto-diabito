import socket
import threading

port = 8000
# Another way to get the local IP address automatically
host = "127.0.0.1"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))


def handle_client(conn, addr):
    print(f"{addr[0]}:{addr[1]} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(1024).decode("utf-8")
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode("utf-8")
            if msg == "END":
                connected = False
            print(f"{addr[0]}:{addr[1]}> {msg}")
        conn.send("Msg received".encode("utf-8"))

    conn.close()


server.listen()
print(f"Server is listening on {host}")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
