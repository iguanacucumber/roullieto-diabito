import socket
import threading

# Server constants
HOST ="192.168.241.181"
PORT = 5555
BUFFER_SIZE = 1024

# Clients list
clients = []

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    clients.append(client_socket)

    try:
        while True:
            # Receive data from client
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            # Broadcast the data to all other clients
            for client in clients:
                if client != client_socket:
                    client.send(data)
    except:
        print(f"Connection with {addr} lost")
    finally:
        # Remove client from the list
        clients.remove(client_socket)
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)
    print(f"Server started on {HOST}:{PORT}")
    
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()