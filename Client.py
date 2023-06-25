import socket
import json

def handle_request(client_socket):
    # Receive the request from the client.
    request = client_socket.recv(1024).decode('utf-8')

    # Parse the request.
    request_data = json.loads(request)

    # Handle the request.
    if request_data['action'] == 'post':
        # Post a new message.
        post = request_data['post']
        save_post(post)
    elif request_data['action'] == 'get_posts':
        # Get all the posts.
        posts = get_posts()
        client_socket.send(json.dumps(posts).encode('utf-8'))
    elif request_data['action'] == 'send_dm':
        # Send a direct message.
        dm = request_data['dm']
        send_dm(dm)

def main():
    # Create a socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(10)

    while True:
        # Accept a connection from a client.
        client_socket, client_address = server_socket.accept()

        # Handle the request from the client.
        handle_request(client_socket)

if __name__ == '__main__':
    main()
