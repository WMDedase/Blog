import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 6060

LIGHT_GREY = '#F0F0F0'
DARK_GREY = '#707070'
BLUE = '#0099FF'
WHITE = "#ffffff"
FONT = ("Arial", 14)
BUTTON_FONT = ("Arial", 12)
MESSAGE_FONT = ("Arial", 12)

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message, is_user=False):
    message_box.config(state=tk.NORMAL)
    if is_user:
        message_box.insert(tk.END, f"You: {message}\n", "user_message")
    else:
        message_box.insert(tk.END, f"{message}\n", "other_message")
    message_box.config(state=tk.DISABLED)
    message_box.see(tk.END)

def connect(event=None):
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
        add_message("Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_frame.place_forget()  # Hide username frame
    message_frame.pack(expand=True, fill=tk.BOTH)  # Show messaging frame

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message(event=None):
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

root = tk.Tk()
root.geometry("600x600")
root.title("Simple Chat App")
root.resizable(False, False)
root.config(bg=LIGHT_GREY)

# Username Frame
username_frame = tk.Frame(root, bg=LIGHT_GREY, bd=5, relief=tk.GROOVE)
username_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

username_label = tk.Label(username_frame, text="Enter Your Username", font=("Arial", 18, "bold"), bg=LIGHT_GREY, fg=DARK_GREY)
username_label.pack(pady=(10, 5))

username_textbox = tk.Entry(username_frame, font=("Arial", 14), bg=WHITE, fg=DARK_GREY, width=20, bd=2, relief=tk.GROOVE)
username_textbox.pack(pady=5)

username_button = tk.Button(username_frame, text="Join Chat", font=("Arial", 12, "bold"), bg=BLUE, fg=WHITE, height=1, command=connect, bd=2, relief=tk.GROOVE)
username_button.pack(pady=10)

# Bind the <Return> key event to connect function
username_textbox.bind("<Return>", connect)

# Message Frame
message_frame = tk.Frame(root, bg=WHITE, bd=5, relief=tk.GROOVE)
message_frame.pack(expand=True, fill=tk.BOTH)
message_frame.pack_forget()  # Initially hide messaging frame

message_box = scrolledtext.ScrolledText(message_frame, font=MESSAGE_FONT, bg=WHITE, fg=DARK_GREY, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(padx=10, pady=10, ipady=8, ipadx=8, fill=tk.BOTH, expand=True)  # Place the message box

message_textbox = tk.Entry(message_frame, font=("Arial", 14), bg=WHITE, fg=DARK_GREY, bd=2, relief=tk.GROOVE)
message_textbox.pack(pady=10, padx=10, ipady=8, ipadx=8, fill=tk.X)  # Centered message textbox with padding

# Bind the <Return> key event to send_message function
message_textbox.bind("<Return>", send_message)

# Configure tags for message box
message_box.tag_configure("user_message", foreground=BLUE)
message_box.tag_configure("other_message", foreground=DARK_GREY)

def listen_for_messages_from_server(client):
    while 1:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]

                add_message(f"[{username}] {content}", is_user=(username == username_textbox.get()))
            else:
                messagebox.showerror("Error", "Message received from the client is empty")
        except:
            break

# Main function
def main():
    root.mainloop()

if __name__ == '__main__':
    main()
