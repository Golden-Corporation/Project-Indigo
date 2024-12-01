from ascii_magic import AsciiArt, load_from_file

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    authenticated = False
    username = None

    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                break

            if msg.startswith("SIGNUP"):
                _, username, password = msg.split(":")
                if username in users:
                    conn.send("Username already exists.".encode('utf-8'))
                else:
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    users[username] = hashed_password
                    post_history[username] = []  # Initialize an empty list for user's post history
                    save_credentials()
                    save_message_history()  # Save updated history to file
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

                    # Attempt to convert the image to ASCII art with a smaller resolution
                    ascii_art = ""
                    try:
                        ascii_art = AsciiArt.from_image(image_path, columns=50).to_ascii()  # Smaller size
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

                    save_message_history()  # Save updated history to file
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
        except Exception as e:
            print(f"[ERROR] {e}")
            break

    conn.close()
    print(f"[DISCONNECT] {addr} disconnected.")
