import random
import os

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
    print("Welcome to Project Indigo (Beta)")

    # Create the file if it doesn't exist
    if not os.path.exists("identification.txt"):
        with open("identification.txt", "w") as f:
            f.write("")

    # Read the identification number from the file
    with open("identification.txt", "r") as f:
        number = f.read()

    # Create the friends list
    friends_list = []

    # Handle the user's choice
    while True:
        print("1. Posts")
        print("2. Make a post")
        print("3. DMs")
        print("4. Receive DMs")
        print("5. Identification")
        print("6. Friends List")

        # Get the user's choice
        choice = input("Enter your choice: ")

        if choice == "1":
            posts = get_posts()
            for post in posts:
                # Add the user's number to the post
                post = f"{post} - User{post.split('-')[0]}"
                print(post)
        elif choice == "2":
            message = input("Enter your message: ")
            post_message(message)
        elif choice == "3":
            sender_number = input("Enter your number: ")
            recipient_number = input("Enter the recipient's number: ")
            message = input("Enter your message: ")
            send_dm(sender_number, recipient_number, message)
        elif choice == "4":
            print("You can now receive DMs")
        elif choice == "5":
            identification_page()
        elif choice == "6":
            # Show the friends list
            for friend in friends_list:
                print(f"User{friend}")

            # Add a friend to the list
            friend_number = input("Enter the friend's number: ")
            friends_list.append(friend_number)
        else:
            print("Invalid choice")

def show_posts():
    posts = get_posts()
    for post in posts:
        print(post)

if __name__ == "__main__":
    main()
