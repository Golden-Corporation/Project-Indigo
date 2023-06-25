
import os
import socket

def get_posts():
    posts = []
    with open("posts.txt", "r") as f:
        for line in f:
            posts.append(line.strip())
    return posts

def post_message(message):
    with open("posts.txt", "a") as f:
        f.write(message + "\n")

def send_dm(username, message):
    with open("dms.txt", "a") as f:
        f.write(f"{username}: {message}\n")

def main():
    posts = get_posts()
    for post in posts:
        print(post)

    while True:
        message = input("Enter a message: ")
        if message == "exit":
            break
        else:
            post_message(message)

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    host = "localhost"
    port = 8000
    sock.bind((host, port))

    # Listen for connections
    sock.listen(5)

    # Accept a connection
    connection, address = sock.accept()

    # Receive data from the client
    data = connection.recv(1024)

    # Print the data
    print(data.decode())

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()
