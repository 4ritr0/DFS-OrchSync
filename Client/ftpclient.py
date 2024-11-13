#!/usr/bin/env python3
import ssl
from socket import AF_INET, SOCK_STREAM, socket
import threading
import os
# Functions for sending and receiving messages
def send_message():
    message = input("Enter message to send: ")
    if message:
        try:
            ssl_sock.sendall(message.encode("utf-8"))
            response = ssl_sock.recv(1024).decode("utf-8")
            print("Server response:", response.upper())
        except Exception as e:
            print("Error:", e)
    else:
        print("Please enter a message.")

def get_file():
    filename = input("Enter filename to download: ")
    if filename:
        try:
            ssl_sock.sendall(f"GET {filename}".encode("utf-8"))
            first = ssl_sock.recv(1024)
            if first.startswith(b"ERROR:"):
                print(first.decode("utf-8"))
                return 
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in ['.jpg','.jpeg','.png']:
                with open(filename, 'wb') as outfile:
                    outfile.write(first)
                    while True:
                        data = ssl_sock.recv(1024)
                        if b"EOF-STOP" in data:
                            stop_point = data.find(b"EOF-STOP")
                            outfile.write(data[:stop_point])        
                            break        
                        outfile.write(data)
            else:
                with open(filename, 'w') as outfile:
                    while True:
                        data = ssl_sock.recv(1024).decode("utf-8")
                        if "EOF-STOP" in data:
                            stop_point = data.find("EOF-STOP")
                            outfile.write(data[:stop_point])        
                            break        
                        outfile.write(data)
                    
            print(f"File '{filename}' downloaded successfully.")
        except Exception as e:
            print("Error:", e)
                
    else:
        print("Please enter a filename.")
           

def put_file():
    filename = input("Enter filename to upload: ")
    if filename:
        try:
            ssl_sock.sendall(f"PUT {filename}".encode("utf-8"))
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in ['.jpg','.jpeg','.png']:
                with open(filename, 'rb') as infile:
                    for line in infile:
                        ssl_sock.sendall(line)
                ssl_sock.sendall("EOF-STOP".encode('utf-8'))
            else:
                with open(filename, 'r') as infile:
                    print("file opened")
                    for line in infile:
                        ssl_sock.sendall(line.encode('utf-8'))
                ssl_sock.sendall("EOF-STOP".encode('utf-8'))
            
            print(f"File '{filename}' uploaded successfully.")
        except Exception as e:
            print("Error:", e)
    else:
        print("Please enter a filename.")

def view_file():
    filename = input("Enter filename to view: ")
    if filename:
        try:
            ssl_sock.sendall(f"VIEW {filename}".encode("utf-8"))
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension in ['.jpg','.jpeg','.png']:
                    data = ssl_sock.recv(1024)
                    print(f"First 1024 bytes of '{filename}':")
                    # if b"EOF-STOP" in data:
                    #     stop_point = data.find(b"EOF-STOP")
                    #     print(data[:stop_point]) 
                    print(data)       
            else:
                    data = ssl_sock.recv(1024).decode("utf-8")
                    print(f"First 1024 bytes of '{filename}':")
                    # if "EOF-STOP" in data:
                    #     stop_point = data.find("EOF-STOP")
                    #     print(data[:stop_point])  
                    print(data)             
        except Exception as e:
            print("Error:", e)
                
    else:
        print("Please enter a filename.")


def delete_file():
    filename = input("Enter filename to delete: ")
    if filename:
        try:
            ssl_sock.sendall(f"DELETE {filename}".encode("utf-8"))
            response = ssl_sock.recv(1024).decode("utf-8")
            print(response)
        except Exception as e:
            print("Error:", e)
    else:
        print("Please enter a filename.")

def list_files():
    try:
        ssl_sock.sendall("LIST".encode("utf-8"))
        while True:
            response = ssl_sock.recv(1024).decode("utf-8")
            if "EOF-STOP" in response:
                stop_point = response.find("EOF-STOP")
                print(response[:stop_point])        
                break        
            print(response)
    except Exception as e:
        print("Error:", e)

def quit_connection():
    try:
        ssl_sock.sendall("QUIT".encode("utf-8"))
        ssl_sock.close()
        print("Connection closed.")
    except Exception as e:
        print("Error:", e)


def quit_connection():
    try:
        ssl_sock.sendall("QUIT".encode("utf-8"))
        ssl_sock.close()
        print("Connection closed.")
    except Exception as e:
        print("Error:", e)

# Setup secure connection
HOST = '127.0.0.1'
PORT = 21

sock = socket(AF_INET, SOCK_STREAM)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE 
ssl_sock = ssl_context.wrap_socket(sock)
ssl_sock.connect((HOST, PORT))

# Main loop for command-line interface
def main():
    while True:
        print("\nOptions:")
        print("1. Send a message")
        print("2. Get a file")
        print("3. Put a file")
        print("4. View a file")
        print("5. Delete a file")
        print("6. List files")
        print("7. Quit")

        choice = input("Choose an option (1-7): ")
        if choice == '1':
            send_message()
        elif choice == '2':
            get_file()
        elif choice == '3':
            put_file()
        elif choice == '4':
            view_file()
        elif choice == '5':
            delete_file()
        elif choice == '6':
            list_files()
        elif choice=='7':
            quit_connection()
            break
        else:
            print("Invalid choice. Please choose again.")

# Run the command-line interface
if __name__ == "__main__":
    main()