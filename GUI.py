import tkinter as Tk

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

    # Run the main loop
    root.mainloop()


if __name__ == "__main__":
    main()

