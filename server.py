#sever
import socket 
import os
import time
import struct
HOST = "172.20.10.2"
PORT = 65432

borderline = "---///---/ongquatronroido//--xichlendumtuidi-///=="
borderline_b = borderline.encode('utf-8')

def sendFileList(client_socket):
    with open("data.txt", "r") as file:
       while True:
            chunk = file.read(1024)  
            if not chunk:
                break  
            client_socket.sendall(chunk.encode('utf-8'))
    client_socket.sendall(borderline.encode('utf-8'))

def sizeFile(file_name):
    with open(file_name, "rb") as file:
        file.seek(0, 2)
        file_size = file.tell()
        file.close()
    return file_size


def sendFile(client_socket, file_name):
    size = sizeFile(file_name)
    try:
        with open(file_name, "rb") as file:
            file_size_bytes = struct.pack('!I', size)
            client_socket.sendall(file_size_bytes)

            while True:
                data = file.read(10240)
                if not data:
                    break
                client_socket.sendall(data)
                            
    except FileNotFoundError:
        print(f"File {file_name} not found on the server.")

def sendMultipleFile(client_socket, file_names):
    try:
        for file_name in file_names:
            sendFile(client_socket, file_name)
    except KeyboardInterrupt:
        client_socket.close()

def receiveRequest(client_socket):
    data = ""
    while True:
        chunk = client_socket.recv(1024).decode('utf-8')
        if not chunk: 
            break
        if borderline in chunk:
            data += chunk.split(borderline, 1)[0]
            break   
        data += chunk
    file_names = extractRequest(data)
    return file_names

def extractRequest(chunk):  
    lines = chunk.strip().split('\n')
    file_names = []
    
    for line in lines:
        name = line.strip()
        if name:
            file_names.append(name)
    
    return file_names

def serveClient(client_socket):
    try:
        while True:
            file_names = receiveRequest(client_socket)
            if not file_names:
                break
            sendMultipleFile(client_socket, file_names)
            print("All requested files sent.")
    except ConnectionResetError:
        print("Connection Error!")
    finally:
        client_socket.close()
        print("Client disconnected.")



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    try:
        while True:
            #tùy chỉnh clear cho cả Windows và MacOs/Linux
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Waiting for client...")
            client_socket, client_address = server_socket.accept() 
            print(f"Client connected from {client_address}")
            sendFileList(client_socket) 
            serveClient(client_socket)
    except KeyboardInterrupt:
        print("Stopping the server...")
        server_socket.close()
        print("Server stopped.")
   
if __name__ == "__main__":
    main()
