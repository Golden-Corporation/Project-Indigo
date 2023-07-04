import random
import socket

MULTICAST_IP = "224.0.0.1"
MULTICAST_PORT = 8080

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.bind(('', MULTICAST_PORT))

client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.INADDR_ANY)
client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

while True:
    # Get the user's input
    message = input("Enter your message: ")

    # Send the message to the multicast group
    client_socket.sendto(message.encode("utf-8"), (MULTICAST_IP, MULTICAST_PORT))

    # Receive a message from the server
    data, address = client_socket.recvfrom(1024)

    # Print the message
    print(data.decode("utf-8"))

def show_posts():
    posts = get_posts()
    for post in posts:
        # Add the user's number to the post
        post = f"{post} - User{post.split('-')[0]}"
        print(post)

def send_dm(sender_number, recipient_number, message):
    with open("dms.txt", "a") as f:
        f.write(f"{sender_number}: {recipient_number}: {message}\n")

if __name__ == "__main__":
    main()
