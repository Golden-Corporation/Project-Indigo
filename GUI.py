import tkinter as Tk
from tkinter import Listbox

def get_posts():
    posts = []

    with open("posts.txt", "r") as f:
        for line in f:
            posts.append(line.strip())

    return posts

def main():
    root = Tk.Tk()
    root.title("Project Indigo")

    # Create the posts list
    posts_list = Listbox(root)
    posts_list.pack()

    # Create the buttons
    show_posts_button = Button(root, text="Show Posts", command=show_posts)
    show_posts_button.pack()

    make_post_button = Button(root, text="Make Post", command=make_post)
    make_post_button.pack()

    send_dm_button = Button(root, text="Send DM", command=send_dm)
    send_dm_button.pack()

    # Run the main loop
    root.mainloop()

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

def post_message(message):
    with open("posts.txt", "a") as f:
        f.write(f"{message}-\n")

def send_dm(sender_number, recipient_number, message):
    pass


if __name__ == "__main__":
    main()
