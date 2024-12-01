import socket
import ascii_magic
from colorama import init

# Initialize colorama
init(autoreset=True)

# Constants for server connection
SERVER_ADDRESS = ('192.168.0.157', 8080)  # Change to your server address
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    client.connect(SERVER_ADDRESS)
    print("Connected to the server.")

def signup():
    username = input("Enter username: ")
    password = input("Enter password: ")
    client.send(f"SIGNUP:{username}:{password}".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    client.send(f"LOGIN:{username}:{password}".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))
    return username

def post_content(username):
    content = input("Enter your text post (or leave empty to skip): ")
    add_image = input("Do you want to add an image? (y/n): ").lower()
    ascii_art = ""

    if add_image == "y":
        image_path = input("Enter the path to your image: ")
        try:
            # Create ASCII art from the image
            my_art = ascii_magic.AsciiArt.from_image(image_path)
            ascii_art = str(my_art)  # Convert ASCII art to a string
        except Exception as e:
            print(f"Failed to convert image: {e}")
            return

    # Send both text and ASCII art (if present) to the server
    client.send(f"POST:{content}:{ascii_art}".encode('utf-8'))
    print(client.recv(1024).decode('utf-8'))

def get_posts():
    client.send("GET_POSTS".encode('utf-8'))
    posts = client.recv(4096).decode('utf-8')
    print("Posts:\n", posts)

def main():
    connect()
    action = input("Do you want to sign up or login? (signup/login): ").strip().lower()
    
    if action == "signup":
        signup()
    username = login()

    while True:
        print("\nMenu:\n1. Post content\n2. Get posts\n3. Disconnect")
        choice = input("Choose an option: ")
        
        if choice == '1':
            post_content(username)
        elif choice == '2':
            get_posts()
        elif choice == '3':
            client.send("DISCONNECT".encode('utf-8'))
            break
        else:
            print("Invalid option. Please try again.")

    client.close()

if __name__ == "__main__":
    main()
