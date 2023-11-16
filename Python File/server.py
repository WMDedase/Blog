# Import required modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 6060  # You can use any port between 0 to 65535
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):

    while 1:
        try:
            message = client.recv(2048).decode('utf-8')
            if not message:
                break  # Break the loop if the client disconnects
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        except (ConnectionAbortedError, ConnectionResetError):
            print(f"Connection with client {username} unexpectedly terminated.")
            remove_client(username)
            break

# Function to send message to a single client
def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except (ConnectionAbortedError, ConnectionResetError):
        print("Error sending message to client. Client may have disconnected unexpectedly.")

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    try:
        while 1:
            username = client.recv(2048).decode('utf-8')
            if username != '':
                active_clients.append((username, client))
                prompt_message = "SERVER~" + f"{username} added to the chat"
                send_messages_to_all(prompt_message)
                break
            else:
                print("Client username is empty")

        threading.Thread(target=listen_for_messages, args=(client, username,)).start()

    except (ConnectionAbortedError, ConnectionResetError):
        print("Connection with a new client unexpectedly terminated.")

# Function to remove a client from the active_clients list
def remove_client(username):
    for user in active_clients:
        if user[0] == username:
            active_clients.remove(user)
            print(f"Client {username} removed from the active clients list.")

# Main function
def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:
        try:
            client, address = server.accept()
            print(f"Successfully connected to client {address[0]} {address[1]}")
            threading.Thread(target=client_handler, args=(client,)).start()

        except (ConnectionAbortedError, ConnectionResetError):
            print("Error accepting a new client. Connection may have been unexpectedly terminated.")

if __name__ == '__main__':
    main()
