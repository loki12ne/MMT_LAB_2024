import socket
import os

HOST = "127.0.0.1"
PORT = 65432

# try:
#     while True:
#         msg = input('Client: ')
#         client.sendall(bytes(msg, "utf8"))
#     # client.sendall(b"This is the message from client")
# except KeyboardInterrupt:
#     client.close()
# finally:
#     client.close()

def receiveFile(client_socket, file_name):
    # Receive file size
    file_size = int(client_socket.recv(1024).decode('utf-8')) #size in megabytes
    file_size *= 1e6 #size in bytes

    # Receive file data by chunk = 1024 bytes
    received_size = 0
    with open(file_name, "wb") as file:
        while received_size < file_size:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
            received_size += 1024

        # Print PROGESSING BAR

def checkFile(files, file_name):
    # Check whether the file exists in the file list
    if file_name not in files:
        return
    
    # Check whether the file has been downloaded
    program_path = os.getcwd()
    file_path = os.path.join(program_path, file_name)
    count = files.count(file_name)

    if os.path.exists(file_path):
        file_name = renameFile(file_name, count)

def renameFile(file_name, count):
    if count == 0:
        return file_name
    
    # Insert number if the file has already been downloaded
    name, ext = os.path.splitext(file_name)
    new_name = f"{name} ({count}){ext}"

    return new_name
    
            

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    client_socket.connect(server_address)

    file_name = "input.txt"
    receiveFile(file_name)

    # close socket 
    client_socket.close()
    # vde là làm s chạy Ctrl + C dưới nền

if __name__ == "__main__":
    main()
