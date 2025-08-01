#!/usr/bin/env python3
import os
import ssl
from socket import AF_INET, SOCK_STREAM, socket

server_storage_path="../Server/server_storage"
password = "Aritro123!@#" 

def get(conn, filename, username):
    try:
        client_dir= os.path.join(server_storage_path, username)
        file_path = os.path.join(client_dir, filename)
        file_extension = os.path.splitext(filename)[1].lower()
        end_message = "EOF-STOP"
        if not os.path.exists(file_path): 
            error_message = b"ERROR: File doesn't exist"
            conn.sendall(error_message)
            return
        if os.path.getsize(file_path) == 0:
            empty_message = b"NOTE: The file is empty."
            conn.sendall(empty_message)
            conn.sendall(end_message.encode('utf-8')) 
            return
        if file_extension in ['.jpg','.jpeg','.png']:
            with open(file_path, 'rb') as infile:
                for line in infile:
                    conn.sendall(line)

            conn.sendall(end_message.encode('utf-8'))
        else:
            with open(file_path, 'r') as infile:
                for line in infile:
                    conn.sendall(line.encode('utf-8'))
            conn.sendall(end_message.encode('utf-8'))
    except Exception as e:
        print(e)
        #error_message = ("There has been an error sending the requested file. "
        #                 + filename + " might not exist")
        error_message = b"ERROR: File error occured"
        conn.sendall(error_message)


def put(conn, command, username):
    filename = command.split(' ')[1]
    try:
        client_dir = os.path.join(server_storage_path, username)
        if not os.path.exists(client_dir):
            os.makedirs(client_dir)
        file_path = os.path.join(client_dir, filename)
        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension in ['.jpg', '.jpeg', '.png']:
            with open(file_path, 'wb') as outfile:
                while True:
                    data = conn.recv(1024)
                    if b"EOF-STOP" in data:
                        stop_point = data.find(b"EOF-STOP")
                        outfile.write(data[:stop_point])
                        break  # Exit the loop after EOF-STOP
                    outfile.write(data)
        else:
            with open(file_path, 'w') as outfile:
                while True:
                    data = conn.recv(1024).decode("utf-8")
                    if "EOF-STOP" in data:
                        stop_point = data.find("EOF-STOP")
                        outfile.write(data[:stop_point])
                        break  # Exit the loop after EOF-STOP
                    outfile.write(data)

        print("Received File:", filename)
        conn.sendall(b"SUCCESS: File received")

    except Exception as e:
        print(e)
        error_message = "ERROR: There has been an error receiving the requested file."
        conn.sendall(error_message.encode('utf-8'))



def view(conn, data, username):
    filename = data.split(' ')[1]
    try:
        client_dir= os.path.join(server_storage_path, username)
        file_path = os.path.join(client_dir, filename)
        file_extension = os.path.splitext(filename)[1].lower()
        end_message = "EOF-STOP"
        if os.path.getsize(file_path) == 0:
            empty_message = f"NOTE: '{filename}' is empty.".encode("utf-8")
            conn.sendall(empty_message)
            return
        if file_extension in ['.jpg','.jpeg','.png']:
            with open(file_path, 'rb') as infile:
                data= infile.read(1024)
                conn.sendall(data)
            #conn.sendall(end_message.encode('utf-8'))
        else:
            with open(file_path, 'r') as infile:
                data= infile.read(1024)
                conn.sendall(data.encode('utf-8'))
            #conn.sendall(end_message.encode('utf-8'))
    except Exception as e:
        print(e)
        error_message = ("There has been an error sending the requested file. "
                         + filename + " might not exist")
        conn.sendall(error_message.encode('utf-8'))


def delete(conn, data, username):
    filename = data.split(' ')[1]
    try:
        client_dir= os.path.join(server_storage_path, username)
        file_path = os.path.join(client_dir, filename)
        os.remove(file_path)
        response= ("File "+filename+" deleted successfully.")
        conn.sendall(response.encode("utf-8"))
    except FileNotFoundError:
        error_message = f"Error: File '{filename}' does not exist."
        conn.sendall(error_message.encode("utf-8"))
    except Exception as e:
        print(e)
        error_message = ("There has been an error deleting the requested file. "
                         + filename + " might not exist")
        conn.sendall(error_message.encode('utf-8'))

def list_file(conn, username):
    try:
        client_dir= os.path.join(server_storage_path, username)
        files=os.listdir(client_dir)
        file_list = "\n".join(files)
        response = ("Files on server:" +"\n" +file_list +"\n"+"EOF-STOP")
        conn.sendall(response.encode("utf-8"))
    except Exception as e:
        print(e)
        error_message = ("There has been an error listing the requested files.")
        conn.sendall(error_message.encode('utf-8'))

command_list = ["QUIT","CLOSE", "OPEN", "GET","PUT", "VIEW", "LIST", "DELETE"]

HOST = '127.0.0.1' #Change this to the IP address of the server/Host
PORT = 21 #FTP is uauully on port 21 so dont change this

sock = socket(AF_INET, SOCK_STREAM)

#password = input("Enter certificate password: ") 
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.load_cert_chain(certfile="server.cer", keyfile="server.key", password = password)  

ssl_sock = ssl_context.wrap_socket(sock, server_side=True)

ssl_sock.bind((HOST, PORT))

while True:
    ssl_sock.listen()

    conn, addr = ssl_sock.accept()
    print("Connected to ", addr)

    remainder = ""
    while (True):
        command = ""
        if remainder == "":
            try:
                data = conn.recv(1024).decode("utf-8")
                command = data.split(' ')[0].upper()
            except UnicodeDecodeError:
                print("Can't decode binary data.")
        else:
            data = remainder
            if remainder is not None:
                try:
                    space = remainder.find(' ')
                except:
                        space = remainder.find(b' ')
            remainder = ""

        if command in command_list:
            if command == "QUIT":
                print("Client quitting")
                #conn.sendall(command.encode("utf-8"))
                conn.close()
                break

            if command == "OPEN":
                port = int(data.split(' ')[1])
                
                message = "Binding to Port " + str(port)
                print("Binding to Port ", str(port))
                conn.sendall(message.encode('utf-8'))

                ssl_sock.close()

                sock2 = socket(AF_INET, SOCK_STREAM)
                sock2.bind((HOST, port))
                sock2.listen(1)
                conn2, addr2 = sock2.accept()
                print("Connected to ", addr2)

                ssl_sock = ssl_context.wrap_socket(sock2, server_side=True)
                conn = conn2
                continue


            if command == "GET":
                filename = data.split(' ')[1]
                get(conn, filename, username='abc')

            if command == "PUT":
                remainder = put(conn, data, username='abc')
            if command == "VIEW":
                view(conn, data, username='abc')
            if command == "LIST":
                list_file(conn, username='abc')
            if command == "DELETE":
                delete(conn, data, username='abc')
            

        else:
            if data is not None:
                print(data)
                try:
                    conn.sendall(data.upper().encode("utf-8"))
                except:
                    conn.sendall(data.upper())

    print("Disconnected from:", addr)
  
ssl_sock.close()