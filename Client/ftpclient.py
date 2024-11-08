import tkinter as tk
from tkinter import messagebox
import ssl
from socket import AF_INET, SOCK_STREAM, socket
import threading

def send_message():
    message = message_entry.get()
    if message:
        try:
            ssl_sock.sendall(message.encode("utf-8"))
            response = ssl_sock.recv(1024).decode("utf-8")
            response_label.config(text=response.upper())
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please enter a message.")

def handle_get():
    threading.Thread(target=get_file).start()

def get_file():
    filename = file_entry.get()
    if filename:
        try:
            ssl_sock.sendall(f"GET {filename}".encode("utf-8"))
            data = ssl_sock.recv(1024).decode("utf-8")
            with open(filename, 'w') as outfile:
                while data:
                    outfile.write(data)
                    data = ssl_sock.recv(1024).decode("utf-8")
                    if "EOF-STOP" in data:
                        stop_point = data.find("EOF-STOP")
                        outfile.write(data[:stop_point])
                        break
            messagebox.showinfo("Success", f"File {filename} downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please enter a filename.")

def handle_put():
    threading.Thread(target=put_file).start()

def put_file():
    filename = file_entry.get()
    if filename:
        try:
            ssl_sock.sendall(f"PUT {filename}".encode("utf-8"))
            with open(filename, 'r') as infile:
                for line in infile:
                    ssl_sock.sendall(line.encode('utf-8'))
            end_message = "EOF-STOP"
            ssl_sock.sendall(end_message.encode('utf-8'))
            messagebox.showinfo("Success", f"File {filename} uploaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "Please enter a filename.")

def quit_connection():
    try:
        ssl_sock.sendall("QUIT".encode("utf-8"))
        ssl_sock.close()
        root.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))

HOST = '127.0.0.1'
PORT = 12000

sock = socket(AF_INET, SOCK_STREAM)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE 
ssl_sock = ssl_context.wrap_socket(sock)
ssl_sock.connect((HOST, PORT))

root = tk.Tk()
root.title("FTP Client")

message_label = tk.Label(root, text="Enter message:")
message_label.grid(row=0, column=0, sticky="w")

message_entry = tk.Entry(root, width=30)
message_entry.grid(row=0, column=1)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=0, column=2)

file_label = tk.Label(root, text="File name:")
file_label.grid(row=1, column=0, sticky="w")

file_entry = tk.Entry(root, width=30)
file_entry.grid(row=1, column=1)

get_button = tk.Button(root, text="Get", command=handle_get)
get_button.grid(row=1, column=2, padx=5)

put_button = tk.Button(root, text="Put", command=handle_put)
put_button.grid(row=1, column=3, padx=5)

quit_button = tk.Button(root, text="Quit", command=quit_connection)
quit_button.grid(row=2, column=2, columnspan=2, pady=10)

response_label = tk.Label(root, text="")
response_label.grid(row=3, column=0, columnspan=4)

root.mainloop()
