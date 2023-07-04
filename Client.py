import random
import socket
import threading

def send_message():
    # Get the message from the user
    message = input("Enter your message: ")

    # Send the message to the server
    client_socket.sendto(message.encode("utf-8"), (MULTICAST_IP, MULTICAST_PORT))

    # Go back to the main menu
    print("Message sent!")

def receive_message():
    # Receive a message from the server
    data, address = client_socket.recvfrom(1024)

    # Print the message
    print(data.decode("utf-8"))

def main():
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client_socket.bind(('', MULTICAST_PORT))

    # Join the multicast group
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.INADDR_ANY)
    client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Create a thread to receive messages
    receive_message_thread = threading.Thread(target=receive_message)
    receive_message_thread.daemon = True
    receive_message_thread.start()

    # Start the main loop
    while True:
        # Print the menu options
        print("Welcome To Project Indigo")
        print("1) Make a post")
        print("2) Send/Receive DM")
        print("3) See your reference number")
        print("4) Friends")

        # Get the user's choice
        choice = input("Enter your choice: ")

        # Do the corresponding action
        if choice == "1":
            # Make a post
            print("Making a post...")
        elif choice == "2":
            # Send/Receive DM
            print("Sending/Receiving DM...")
        elif choice == "3":
            # See your reference number
            print("Your reference number is:")
        elif choice == "4":
            # Friends
            print("Friends...")
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
