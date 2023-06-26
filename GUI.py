import random
import os
from tkinter import *

def get_posts():
    posts = []
    with open("posts.txt", "r") as f:
        for line in f:
            posts.append(line.strip())
    return posts

def post_message(message):
    with open("posts.txt", "a") as f:
        f.write(message + "\n")

def send_dm(sender_number, recipient_number, message):
    if not isinstance(sender_number, int) or not isinstance(recipient_number, int):
        raise ValueError("The sender_number and recipient_number must be integers")

    with open("dms.txt", "a") as f:
        f.write(f"{sender_number}: {recipient_number}: {message}\n")

def get_username(number):
    with open("accounts.txt", "r") as f:
        for line in f:
            if number == line.split(":")[0]:
                return line.split(":")[1]
    return None

def identification_page():
    number = generate_number()

    with open("identification.txt", "w") as f:
        f.write(str(number))
    print(f"Your identification number is: {number}")

def generate_number():
    return random.randint(0, 999)

def main():
    root = Tk()
    root.title("Project Indigo")

    # Create the posts list
    posts = get_posts()

    # Create the friends list
    friends_list = []

    def show_posts():
        # Clear the posts list
        posts_list.delete(0, END)

        # Add the posts to the list
        for post in posts:
            # Add the user's number to the post
            post = f"{post} - User{post.split('-')[0]}"
            posts_list.insert(END, post)

    def make_post():
        message = input("Enter your message: ")
        post_message(message)
        show_posts()

    def send_dm():
        sender_number = input("Enter your number: ")
        recipient_number = input("Enter the recipient's number: ")
        message = input("Enter your message: ")
        send_dm(sender_number, recipient_number, message)

    def identification_page():
        number = generate_number()

        with open("identification.txt", "w") as f:
            f.write(str(number))
        print(f"Your identification number is: {number}")

    def add_friend():
        friend_number = input("Enter the friend's number: ")
        friends_list.append(friend_number)

    # Create the posts list
    posts_list = Listbox(root)
    posts_list.pack()

    # Create the buttons
    show_posts_button = Button(root, text="Show Posts", command=show_posts)
    show_posts_button.pack()

    make_post_button = Button(root, text="Make Post", command=make_post)
    make_post_button.pack()

    send_dm_button = Button(root, text="Send DM", command=send_dm)
