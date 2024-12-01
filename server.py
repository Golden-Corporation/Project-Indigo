import socket
import threading
import hashlib
import json
from cryptography.fernet import Fernet
import os
from ascii_magic import AsciiArt  # Importing AsciiArt

HOST = '192.168.0.157'  # Listen on all interfaces
PORT = 8080  # Port to listen on

# Define file for storing encrypted user credentials
CREDENTIALS_FILE = 'credentials.json'

# Key for encryption/decryption
if not os.path.exists('secret.key'):
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
else:
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()

cipher_suite = Fernet(key)

# Storage for users and posts (both text and ASCII images)
users = {}  # Format: {"username": "hashed_password"}
posts = []  # Each post is a dictionary with keys: "username", "content" (text), and "image" (ASCII)
post_history = {}  # Format: {"username": [list_of_posts]}

def load_credentials():
    global users
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as file:
            encrypted_data = json.load(file)
            for username, encrypted_password in encrypted_data.items():
                decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                users[username] = decrypted_password

def save_credentials():
    encrypted_data = {username: cipher_suite.encrypt(password.encode()).decode() for username, password in users.items()}
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump(encrypted_data, file)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    authenticated = False
    username = None

    while True:
        msg = conn.recv(1024).decode('utf-8')
        
        if msg.startswith("SIGNUP"):
            _, username, password = msg.split(":")
            if username in users:
                conn.send("Username already exists.".encode('utf-8'))
            else:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                users[username] = hashed_password
                post_history[username] = []  # Initialize an empty list for user's post history
                save_credentials()  # Save credentials to file
                conn.send("Signup successful!".encode('utf-8'))

        elif msg.startswith("LOGIN"):
            _, username, password = msg.split(":")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if users.get(username) == hashed_password:
                authenticated = True
                conn.send("Login successful!".encode('utf-8'))
            else:
                conn.send("Login failed. Invalid username or password.".encode('utf-8'))

        elif authenticated:
            if msg == "DISCONNECT":
                break
            elif msg.startswith("POST"):
                # Expecting format: POST:<content>:<image_path>
                _, post_content, image_path = msg.split(":", 2)

                # Attempt to convert the image to ASCII art
                ascii_art = ""
                try:
                    ascii_art = AsciiArt.from_image(image_path).to_ascii()
                except Exception as e:
                    ascii_art = f"Failed to convert image: {str(e)}"
                
                post_data = {
                    "username": username,
                    "content": post_content if post_content else None,
                    "image": ascii_art if ascii_art else None
                }
                posts.append(post_data)
                
                # Ensure post history is initialized
                if username not in post_history:
                    post_history[username] = []
                post_history[username].append(post_data)  # Save post to user's history
                conn.send("Post added!".encode('utf-8'))
            elif msg == "GET_POSTS":
                all_posts = []
                for post in posts:
                    art_str = post['image'] if post['image'] else ''
                    all_posts.append(f"{post['username']}:\n{post['content']}\n{art_str}")
                all_posts_output = "\n\n".join(all_posts)
                conn.send(all_posts_output.encode('utf-8'))
            elif msg == "GET_HISTORY":
                if username in post_history:
                    history_posts = []
                    for post in post_history[username]:
                        art_str = post['image'] if post['image'] else ''
                        history_posts.append(f"{post['username']}:\n{post['content']}\n{art_str}")
                    history_output = "\n\n".join(history_posts)
                    conn.send(history_output.encode('utf-8'))
                else:
                    conn.send("No post history found.".encode('utf-8'))
            else:
                conn.send("Invalid command".encode('utf-8'))
        else:
            conn.send("Please login or sign up first.".encode('utf-8'))

    conn.close()
    print(f"[DISCONNECT] {addr} disconnected.")

def start():
    load_credentials()  # Load users on server start
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start()

