import socket

def broadcast(message):
    for client in clients:
        client.sendall(message.encode("utf-8"))

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8080))
    server.listen(1)

    clients = []

    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)

        print(f"Client connected from {address}")

        while True:
            # Receive a message from the client
            data = client_socket.recv(1024)

            # Broadcast the message to all of the clients
            broadcast(data)

        client_socket.close()

if __name__ == "__main__":
    main()
