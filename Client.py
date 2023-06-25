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

def send_dm(username, message):
    with open("dms.txt", "a") as f:
        f.write(f"{username}: {message}\n")

def main():
    posts = get_posts()
    for post in posts:
        print(post)

    while True:
        message = input("Enter a message: ")
        if message == "exit":
            break
        else:
            post_message(message)

if __name__ == "__main__":
    main()

