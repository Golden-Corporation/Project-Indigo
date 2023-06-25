import tkinter as tk

root = tk.Tk()
root.title("Project Indigo (Beta)")

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

def show_posts():
    posts = get_posts()
    for post in posts:
        label = tk.Label(root, text=post)
        label.pack()

def main():
    show_posts()

    button = tk.Button(root, text="Post Message", command=lambda: post_message(input("Enter a message: ")))
    button.pack()

    button = tk.Button(root, text="Send DM", command=lambda: send_dm(input("Enter a username: "), input("Enter a message: ")))
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
