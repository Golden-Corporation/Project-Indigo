
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
    print("Welcome to Project Indigo (Beta)")

    # Create a sidebar
    print("1. Posts")
    print("2. DMs")
    print("3. Profile")

    # Get the user's choice
    choice = input("Enter your choice: ")

    # Handle the user's choice
    while choice != "0":
        if choice == "1":
            show_posts()
        elif choice == "2":
            send_dm()
        elif choice == "3":
            profile()
        else:
            print("Invalid choice")

        # Go back to the main menu
        choice = input("Enter your choice: ")

def show_posts():
    posts = get_posts()
    for post in posts:
        print(post)

def send_dm():
    username = input("Enter the username: ")
    message = input("Enter the message: ")
    send_dm(username, message)

def profile():
    print("This is your profile")

if __name__ == "__main__":
    main()

