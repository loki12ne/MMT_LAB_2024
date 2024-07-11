import socket
import os

HOST = "127.0.0.1"
PORT = 65432

# File size is expected to be converted to bytes
def receiveFile(client_socket, file_name, file_size):
    # Receive file size
    # file_size = int(client_socket.recv(1024).decode('utf-8')) #size in megabytes
    # file_size *= 1e6 #size in bytes

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

# Check whether the file exists in the file list
def isValidFile(files, file_name):
    if file_name not in files:
        return False, -1 #-1 là index, idx = -1 thì file ko tồn tại trong mảng
    else:
        return True, files.index(file_name) #trả về idx của file_name để cập nhật file_size lun
        
def checkFileExistence(files, file_name):
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

    files_list = "input.txt" #jj đó

    try:
        while True:
            # READ FILE LIST -> return file_names[], file_sizes[] (?)
            file_name = input('Enter a file name: ')
            client_socket.send(bytes(file_name, "utf8"))
            
            flag, i = isValidFile(file_names, file_name) #ktra ten file client nhap vao co ton tai
            if flag:
                file_size = file_sizes[i]
                file_name = checkFileExistence(file_names, file_name) # ktra lai dong nay
                receiveFile(client_socket, file_name, file_size)
            else:
                pass
        
    except KeyboardInterrupt:
        client_socket.close()
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
