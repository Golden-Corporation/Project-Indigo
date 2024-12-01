import socket
import os
from ascii_magic import AsciiArt

SERVER = "127.0.0.1"  # Change to server's IP if running on a remote machine
PORT = 8080  # Must match the server's port


class SocialMediaClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (SERVER, PORT)

    def connect(self):
        try:
            self.client_socket.connect(self.server_address)
            print("Connected to the server.")
        except ConnectionRefusedError:
            print("Failed to connect to the server. Please ensure the server is running.")
            exit()

    def send(self, message):
        self.client_socket.send(message.encode('utf-8'))

    def receive(self):
        return self.client_socket.recv(4096).decode('utf-8')

    def signup(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        self.send(f"SIGNUP:{username}:{password}")
        response = self.receive()
        print(response)

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        self.send(f"LOGIN:{username}:{password}")
        response = self.receive()
        if "successful" in response:
            print("Login successful!")
            return True
        else:
            print("Login failed.")
            return False

    def post_content(self):
        text_content = input("Enter your text post (or leave empty to skip): ")
        add_image = input("Do you want to add an image? (y/n): ").lower()
        image_path = ""

        if add_image == 'y':
            image_path = input("Enter the path to your image: ")
            if not os.path.exists(image_path):
                print("Invalid image path.")
                return

        self.send(f"POST:{text_content}:{image_path}")
        response = self.receive()
        print(response)

    def get_posts(self):
        self.send("GET_POSTS")
        posts = self.receive()
        print("\nPosts:\n" + posts)

    def get_post_history(self):
        self.send("GET_HISTORY")
        history = self.receive()
        print("\nYour Post History:\n" + history)

    def menu(self):
        while True:
            print("\nMenu:")
            print("1. Post content")
            print("2. Get posts")
            print("3. Get post history")
            print("4. Disconnect")
            choice = input("Choose an option: ")

            if choice == "1":
                self.post_content()
            elif choice == "2":
                self.get_posts()
            elif choice == "3":
                self.get_post_history()
            elif choice == "4":
                self.send("DISCONNECT")
                print("Disconnected from the server.")
                break
            else:
                print("Invalid option.")

    def run(self):
        self.connect()
        while True:
            action = input("Do you want to sign up or login? (signup/login): ").lower()
            if action == "signup":
                self.signup()
            elif action == "login":
                if self.login():
                    self.menu()
                    break
            else:
                print("Invalid option. Please enter 'signup' or 'login'.")


if __name__ == "__main__":
    client = SocialMediaClient()
    client.run()
