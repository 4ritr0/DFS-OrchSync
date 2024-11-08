import ssl
from socket import AF_INET, SOCK_STREAM, socket

password = "****" #Change this to the password you set your certificate with 

def get(conn, filename):
    try:
        with open(filename, 'r') as infile:
            for line in infile:
                conn.sendall(line.encode('utf-8'))    
        end_message = "EOF-STOP"
        conn.sendall(end_message.encode('utf-8'))
    except Exception as e:
        print(e)
        error_message = ("There has been an error sending the requested file. "
                         + filename + " might not exist")
        conn.sendall(error_message.encode('utf-8'))


def put(conn, data):
    filename = data.split(' ')[1]
    print("Received File: "+filename)

    try:
        data = conn.recv(1024).decode("utf-8")
        with open(filename, 'w') as outfile:
            while(data):
                outfile.write(data)
                data = conn.recv(1024).decode("utf-8")
                if "EOF-STOP" in data:
                    stop_point = data.find("EOF-STOP")
                    outfile.write(data[:stop_point])
                    return data[stop_point+8:]
    except Exception as e:
        print(e)
        error_message = "There has been an error receiving the requested file."
        conn.sendall(error_message.encode('utf-8'))
        return ""


command_list = ["QUIT","CLOSE", "OPEN", "GET","PUT"]

HOST = '127.0.0.1' #Change this to the IP address of the server/Host
PORT = 21 #FTP is uauully on port 21 so dont change this

sock = socket(AF_INET, SOCK_STREAM)

#password = input("Enter certificate password: ") 
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.load_cert_chain(certfile="../server.cer", keyfile="../server.key", password = password)  

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
            data = conn.recv(1024).decode("utf-8")
            command = data.split(' ')[0].upper()
        else:
            data = remainder
            space = remainder.find(' ')
            command = remainder[:space].upper()
            remainder = ""

        if command in command_list:
            if command == "QUIT":
                print("Client quitting")
                conn.sendall(command.encode("utf-8"))
                conn.close()
                break
            
            if command == "CLOSE":
                print("Client disconnecting")
                conn.sendall(command.encode("utf-8"))
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
                get(conn, filename)

            if command == "PUT":
                remainder = put(conn, data)

        else:
            print(data)
            conn.sendall(data.upper().encode("utf-8"))

    print("Disconnected from:", addr)
  
ssl_sock.close()
