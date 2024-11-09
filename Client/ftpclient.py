import ssl
from socket import AF_INET, SOCK_STREAM, socket
import threading

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
            with open(filename, 'r') as infile:
                for line in infile:
                    ssl_sock.sendall(line.encode('utf-8'))
            ssl_sock.sendall("EOF-STOP".encode('utf-8'))
            print(f"File '{filename}' uploaded successfully.")
        except Exception as e:
            print("Error:", e)
    else:
        print("Please enter a filename.")

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
        print("4. Quit")

        choice = input("Choose an option (1-4): ")
        if choice == '1':
            send_message()
        elif choice == '2':
            get_file()
        elif choice == '3':
            put_file()
        elif choice == '4':
            quit_connection()
            break
        else:
            print("Invalid choice. Please choose again.")

# Run the command-line interface
if __name__ == "__main__":
    main()







