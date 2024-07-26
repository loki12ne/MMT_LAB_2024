import socket
import os
import struct
import sys
import time

HOST = "127.0.0.1"
PORT = 65432
_file = "input.txt"
download_path = "D:\HCMUS\Y1 - S3\MMT\PJ_File-Downloading\SOCKET\SOCKET 1\download"
borderline = "---///---/ongquatronroido//--xichlendumtuidi-///=="
borderline_b = borderline.encode('utf-8')

def gotoXY(x, y):
    print(f"\033[{y};{x}H", end='')

def sendRequest(client_socket, file_names): 
    for name in file_names:                       
        client_socket.send(name.encode('utf-8'))    
        client_socket.send('\n'.encode('utf-8'))  
    client_socket.send(borderline_b)  

def extractFileList(chunk):  
    lines = chunk.strip().split('\n')
    file_names = []
    
    for line in lines:
        file_name = line.strip()
        if file_name:
            file_names.append(file_name)
    return file_names

def getFileList(file_names):
    file_list = []
    for file_name in file_names:
        name, size = file_name.rsplit(' ', 1)
        file_list.append({"name": name, "size": int(size)})
    return file_list

def receiveFileList(client_socket):
    data = ""
    while True:
        chunk = client_socket.recv(1024).decode('utf-8')
        if not chunk: 
            break
        if borderline in chunk:
            data += chunk.split(borderline, 1)[0]
            break
        data += chunk
    file_names = extractFileList(data)
    
    if file_names:
        file_list = getFileList(file_names)
    print(f"File list from server: {HOST}")
    for i in file_names:
        print(i)
    return file_list

def readInput():
    file_names = []
    try:
        with open(_file, 'r') as f:
            for line in f:
                buf = line.strip()
                if buf:
                    file_names.append(buf)
    except FileNotFoundError:
        print(f"File {_file} not found.")
    return file_names

def getSize(file_list, file_name):
    for file in file_list:
        if file["name"] == file_name:
            return file["size"]

def receiveFile(client_socket, file_names, file_list): 
    data_return = []
    for file_name in file_names:
        if isValidFile(file_list, file_name): 
            data_return.append(file_name)

    file_names = data_return
    
    if not file_names:
        return False

    sendRequest(client_socket, file_names)
    count_inter = 1
    
    os.system('cls' if os.name == 'nt' else 'clear')
    gotoXY(0, 0)

    for file_name in file_names:
        received_size = 0        

        file_size_bytes = client_socket.recv(4)
        file_size = struct.unpack('!I', file_size_bytes)[0]
        file_path = os.path.join(download_path, file_name)
        with open(file_path, "wb") as f:
            while True:
                if received_size > file_size - 10240:
                    data = client_socket.recv(file_size - received_size)
                else:
                    data = client_socket.recv(10240)
                received_size += len(data)
                if not data:
                    break
                f.write(data)

                # Progressing bar
                if received_size > file_size:
                    received_size = file_size
                progress = (received_size / file_size) * 100
                gotoXY(0, count_inter)
                print(f'Downloading {file_name} .... {progress:.2f}%        ', end='')
                if (received_size == file_size):
                    break

        count_inter = count_inter + 1
    gotoXY(0, count_inter)    
    return True

def isSupported(file_list, file):
    for i in file_list:
        if file == i["name"]:
            return True
    return False

def isValidFile(file_list, file):                      
    # Check whether the file exists in the file list
    if not isSupported(file_list, file):
        print(f"{file} is not supported.")       
        return False

    # Check whether the file has been downloaded
    program_path = download_path
    file_path = os.path.join(program_path, file)
    if os.path.exists(file_path):
        print(f"{file} has already been downloaded.")  
        return False
    
    # File is valid to download
    return True


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    client_socket.connect(server_address)
    first_time = 1
    success = 0

    try:
        file_list = receiveFileList(client_socket) 
        while True:
            if success:
                print("All requested files received.")
            if first_time:
                input("ENTER to send the requests to server")
            else:
                input("ENTER to send the requests to server again")

            #tùy chỉnh clear cho cả Windows và MacOs/Linux
            os.system('cls' if os.name == 'nt' else 'clear')
            file_names = readInput()
            first_time = 0
            if not file_names:
                client_socket.close()
                break
            if receiveFile(client_socket, file_names, file_list):
                success = 1
              
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Disconnecting from server...")
        client_socket.close()
        print("Disconnected.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
